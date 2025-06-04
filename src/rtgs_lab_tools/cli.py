"""Command-line interface for RTGS Lab Tools."""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import click
import pandas as pd

from .core import Config, DatabaseManager, setup_logging, GitLogger
from .core.exceptions import RTGSLabToolsError, DatabaseError, ConfigError
from .sensing_data import get_raw_data, list_projects, save_data, create_zip_archive
from .sensing_data.file_operations import ensure_data_directory


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--log-file', help='Log to file')
@click.pass_context
def cli(ctx, verbose, log_file):
    """RTGS Lab Tools - Environmental sensing and climate data toolkit."""
    ctx.ensure_object(dict)
    
    # Set up logging
    log_level = "DEBUG" if verbose else "INFO"
    ctx.obj['logger'] = setup_logging(log_level, log_file=log_file)


@cli.command()
@click.option('--project', '-p', help='Project name to query')
@click.option('--list-projects', is_flag=True, help='List all available projects and exit')
@click.option('--setup-credentials', is_flag=True, help='Create template .env file')
@click.option('--start-date', default="2018-01-01", help='Start date (YYYY-MM-DD)')
@click.option('--end-date', help='End date (YYYY-MM-DD), defaults to today')
@click.option('--node-id', help='Comma-separated list of node IDs to query')
@click.option('--output-dir', help='Output directory for data files')
@click.option('--output', type=click.Choice(['csv', 'parquet']), default='csv', help='Output format')
@click.option('--create-zip', is_flag=True, help='Create zip archive with metadata')
@click.option('--retry-count', type=int, default=3, help='Maximum retry attempts')
@click.option('--no-git-log', is_flag=True, help='Disable automatic git logging')
@click.option('--note', help='Note describing the purpose of this data extraction')
@click.pass_context
def data(ctx, project, list_projects, setup_credentials, start_date, end_date, 
         node_id, output_dir, output, create_zip, retry_count, no_git_log, note):
    """Extract sensing data from GEMS database."""
    logger = ctx.obj['logger']
    
    # Initialize GitLogger
    git_logger = None
    if not no_git_log:
        try:
            git_logger = GitLogger(tool_name="data-extraction")
        except Exception as e:
            logger.warning(f"Failed to initialize git logging: {e}")
    
    start_time = datetime.now()
    
    # Handle setup credentials
    if setup_credentials:
        setup_credentials_file()
        return
    
    try:
        # Initialize configuration and database
        config = Config()
        db_manager = DatabaseManager(config)
        
        # Test database connection
        if not db_manager.test_connection():
            logger.error("Failed to connect to database. Please check your configuration and VPN connection.")
            sys.exit(1)
        
        # Handle list projects
        if list_projects:
            projects = list_projects_command(db_manager)
            if projects:
                click.echo("Available projects:")
                for project_name, node_count in projects:
                    click.echo(f"  {project_name} ({node_count} nodes)")
            else:
                click.echo("No projects found.")
            return
        
        # Validate required arguments
        if not project:
            click.echo("Error: --project is required when not listing projects")
            sys.exit(1)
        
        # Set end date default
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Parse node IDs
        node_ids = None
        if node_id:
            node_ids = [n.strip() for n in node_id.split(',')]
        
        # Ensure output directory
        output_directory = ensure_data_directory(output_dir)
        
        # Extract data
        logger.info(f"Extracting data for project: {project}")
        df = get_raw_data(
            database_manager=db_manager,
            project=project,
            start_date=start_date,
            end_date=end_date,
            node_ids=node_ids,
            max_retries=retry_count
        )
        
        if df.empty:
            logger.info("No data found for the specified parameters")
            return
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project.replace(' ', '_')}_{start_date}_to_{end_date}_{timestamp}"
        
        # Save data
        file_path = save_data(df, output_directory, filename, output)
        
        # Create zip archive if requested
        if create_zip:
            zip_path = create_zip_archive(file_path, df, output)
            click.echo(f"Created zip archive: {zip_path}")
        else:
            click.echo(f"Data saved to: {file_path}")
        
        # Print summary
        click.echo(f"Successfully extracted {len(df)} records")
        
        # Create git log if enabled
        if git_logger:
            try:
                operation = f"Extract data from project '{project}'"
                if note:
                    operation += f" - {note}"
                
                parameters = {
                    'project': project,
                    'start_date': start_date,
                    'end_date': end_date,
                    'node_ids': node_ids,
                    'output_format': output,
                    'output_directory': str(output_directory),
                    'create_zip': create_zip,
                    'retry_count': retry_count,
                    'note': note
                }
                
                results = {
                    'success': True,
                    'records_extracted': len(df),
                    'output_file': str(file_path),
                    'start_time': start_time.isoformat(),
                    'end_time': datetime.now().isoformat()
                }
                
                additional_sections = {
                    "Data Summary": f"- **Records**: {len(df)}\n- **Output**: {file_path}\n- **Format**: {output.upper()}"
                }
                
                if create_zip:
                    additional_sections["Archive"] = f"- **Zip Archive**: {zip_path}"
                
                git_logger.log_execution(
                    operation=operation,
                    parameters=parameters,
                    results=results,
                    script_path=__file__,
                    additional_sections=additional_sections
                )
            except Exception as e:
                logger.error(f"Failed to create git log: {e}")
        
    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        click.echo("Run with --setup-credentials to create a template .env file")
        _log_error_to_git(git_logger, "Configuration error", e, start_time, locals())
        sys.exit(1)
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        _log_error_to_git(git_logger, "Database error", e, start_time, locals())
        sys.exit(1)
    except RTGSLabToolsError as e:
        logger.error(f"Error: {e}")
        _log_error_to_git(git_logger, "Application error", e, start_time, locals())
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        _log_error_to_git(git_logger, "Unexpected error", e, start_time, locals())
        sys.exit(1)
    finally:
        if 'db_manager' in locals():
            db_manager.close()


@cli.command()
@click.option('--variables', '-v', multiple=True, required=True, help='ERA5 variables to download')
@click.option('--start-date', required=True, help='Start date (YYYY-MM-DD)')
@click.option('--end-date', required=True, help='End date (YYYY-MM-DD)')
@click.option('--area', help='Bounding box as "north,west,south,east"')
@click.option('--output-file', '-o', help='Output NetCDF file path')
@click.option('--pressure-levels', help='Pressure levels (comma-separated)')
@click.option('--time-hours', help='Specific hours (comma-separated, e.g., "00:00,12:00")')
@click.option('--list-variables', is_flag=True, help='List available variables and exit')
@click.option('--process', is_flag=True, help='Process downloaded data (basic statistics)')
@click.option('--no-git-log', is_flag=True, help='Disable automatic git logging')
@click.option('--note', help='Note describing the purpose of this ERA5 download')
@click.pass_context
def era5(ctx, variables, start_date, end_date, area, output_file, pressure_levels, 
         time_hours, list_variables, process, no_git_log, note):
    """Download and process ERA5 climate data."""
    logger = ctx.obj['logger']
    
    # Initialize GitLogger
    git_logger = None
    if not no_git_log:
        try:
            git_logger = GitLogger(tool_name="era5-data")
        except Exception as e:
            logger.warning(f"Failed to initialize git logging: {e}")
    
    start_time = datetime.now()
    
    try:
        from .gridded_data import ERA5Client, download_era5_data, process_era5_data
        
        if list_variables:
            client = ERA5Client()
            
            click.echo("Available ERA5 single-level variables:")
            single_vars = client.get_available_variables("single-levels")
            for code, desc in single_vars.items():
                click.echo(f"  {code}: {desc}")
            
            click.echo("\nAvailable ERA5 pressure-level variables:")
            pressure_vars = client.get_available_variables("pressure-levels") 
            for code, desc in pressure_vars.items():
                click.echo(f"  {code}: {desc}")
            return
        
        # Parse area if provided
        area_bounds = None
        if area:
            try:
                area_bounds = [float(x.strip()) for x in area.split(',')]
                if len(area_bounds) != 4:
                    raise ValueError()
            except ValueError:
                click.echo("Error: Area must be 'north,west,south,east' (4 comma-separated numbers)")
                sys.exit(1)
        
        # Parse pressure levels if provided
        pressure_list = None
        if pressure_levels:
            try:
                pressure_list = [int(x.strip()) for x in pressure_levels.split(',')]
            except ValueError:
                click.echo("Error: Pressure levels must be comma-separated integers")
                sys.exit(1)
        
        # Parse time hours if provided
        time_list = None
        if time_hours:
            time_list = [x.strip() for x in time_hours.split(',')]
        
        # Download data
        logger.info(f"Downloading ERA5 data: {variables}")
        output_path = download_era5_data(
            variables=list(variables),
            start_date=start_date,
            end_date=end_date,
            area=area_bounds,
            output_file=output_file,
            pressure_levels=pressure_list,
            time_hours=time_list
        )
        
        click.echo(f"ERA5 data downloaded to: {output_path}")
        
        # Basic processing if requested
        if process:
            logger.info("Processing downloaded ERA5 data")
            ds = process_era5_data(output_path)
            
            click.echo(f"\nDataset summary:")
            click.echo(f"  Variables: {list(ds.data_vars)}")
            click.echo(f"  Time range: {ds.time.min().values} to {ds.time.max().values}")
            click.echo(f"  Spatial extent: {ds.latitude.min().values:.2f}°N to {ds.latitude.max().values:.2f}°N, "
                      f"{ds.longitude.min().values:.2f}°E to {ds.longitude.max().values:.2f}°E")
            click.echo(f"  Shape: {ds.dims}")
        
        # Create git log if enabled
        if git_logger:
            try:
                operation = f"Download ERA5 data for variables: {', '.join(variables)}"
                if note:
                    operation += f" - {note}"
                
                parameters = {
                    'variables': list(variables),
                    'start_date': start_date,
                    'end_date': end_date,
                    'area': area,
                    'output_file': output_file,
                    'pressure_levels': pressure_levels,
                    'time_hours': time_hours,
                    'process': process,
                    'note': note
                }
                
                results = {
                    'success': True,
                    'output_file': output_path,
                    'processed': process,
                    'start_time': start_time.isoformat(),
                    'end_time': datetime.now().isoformat()
                }
                
                additional_sections = {
                    "Download Summary": f"- **Variables**: {', '.join(variables)}\n- **Output**: {output_path}\n- **Date Range**: {start_date} to {end_date}"
                }
                
                git_logger.log_execution(
                    operation=operation,
                    parameters=parameters,
                    results=results,
                    script_path=__file__,
                    additional_sections=additional_sections
                )
            except Exception as e:
                logger.error(f"Failed to create git log: {e}")
        
    except Exception as e:
        logger.error(f"ERA5 error: {e}")
        click.echo(f"Error: {e}")
        _log_era5_error_to_git(git_logger, "ERA5 error", e, start_time, locals())
        sys.exit(1)


@cli.command()
@click.option('--file', '-f', required=True, help='CSV file with sensor data')
@click.option('--parameter', '-p', help='Parameter path to plot (e.g., "Data.Devices.0.Temperature")')
@click.option('--node-id', help='Specific node ID to plot')
@click.option('--multi-param', multiple=True, help='Multiple parameters as "node_id,parameter_path"')
@click.option('--output-dir', default='figures', help='Output directory for plots')
@click.option('--output-file', help='Output filename (without extension)')
@click.option('--format', type=click.Choice(['png', 'pdf', 'svg']), default='png', help='Output format')
@click.option('--list-params', is_flag=True, help='List available parameters and exit')
@click.option('--title', help='Plot title')
@click.option('--no-markers', is_flag=True, help='Disable data point markers')
@click.option('--no-git-log', is_flag=True, help='Disable automatic git logging')
@click.option('--note', help='Note describing the purpose of this visualization')
@click.pass_context
def visualize(ctx, file, parameter, node_id, multi_param, output_dir, output_file, 
              format, list_params, title, no_markers, no_git_log, note):
    """Create visualizations from sensor data."""
    logger = ctx.obj['logger']
    
    # Initialize GitLogger
    git_logger = None
    if not no_git_log:
        try:
            git_logger = GitLogger(tool_name="visualization")
        except Exception as e:
            logger.warning(f"Failed to initialize git logging: {e}")
    
    start_time = datetime.now()
    
    try:
        # Import visualization modules
        from .visualization import (
            create_time_series_plot, 
            create_multi_parameter_plot,
            parse_sensor_messages,
            get_available_parameters
        )
        
        # Read CSV file
        df = pd.read_csv(file)
        logger.info(f"Loaded {len(df)} records from {file}")
        
        # Parse sensor messages
        df = parse_sensor_messages(df)
        
        if list_params:
            # List available parameters
            params_by_node = get_available_parameters(df)
            
            click.echo("Available parameters by node:")
            for node, params in params_by_node.items():
                click.echo(f"\n{node}:")
                for param in sorted(params):
                    click.echo(f"  {param}")
            return
        
        if multi_param:
            # Multi-parameter plot
            parameters = []
            for param_spec in multi_param:
                if ',' in param_spec:
                    node, param_path = param_spec.split(',', 1)
                    parameters.append((param_path.strip(), node.strip()))
                else:
                    parameters.append((param_spec.strip(), None))
            
            output_path = create_multi_parameter_plot(
                df=df,
                parameters=parameters,
                title=title,
                output_file=output_file,
                output_dir=output_dir,
                show_markers=not no_markers,
                format=format
            )
            
        elif parameter:
            # Single parameter plot
            node_ids = [node_id] if node_id else None
            
            output_path = create_time_series_plot(
                df=df,
                parameter_path=parameter,
                node_ids=node_ids,
                title=title,
                output_file=output_file,
                output_dir=output_dir,
                show_markers=not no_markers,
                format=format
            )
            
        else:
            click.echo("Error: Must specify --parameter, --multi-param, or --list-params")
            sys.exit(1)
        
        click.echo(f"Plot saved to: {output_path}")
        
        # Create git log if enabled
        if git_logger:
            try:
                if multi_param:
                    operation = f"Create multi-parameter visualization from {file}"
                    param_info = f"Multiple parameters: {', '.join([p[0] for p in parameters])}"
                elif parameter:
                    operation = f"Create time series plot for {parameter} from {file}"
                    param_info = f"Parameter: {parameter}"
                else:
                    operation = f"List parameters from {file}"
                    param_info = "Parameter listing"
                
                if note:
                    operation += f" - {note}"
                
                parameters_dict = {
                    'input_file': file,
                    'parameter': parameter,
                    'node_id': node_id,
                    'multi_param': list(multi_param) if multi_param else None,
                    'output_dir': output_dir,
                    'output_file': output_file,
                    'format': format,
                    'title': title,
                    'show_markers': not no_markers,
                    'note': note
                }
                
                results = {
                    'success': True,
                    'output_file': output_path if 'output_path' in locals() else None,
                    'records_processed': len(df) if 'df' in locals() else 0,
                    'start_time': start_time.isoformat(),
                    'end_time': datetime.now().isoformat()
                }
                
                additional_sections = {
                    "Visualization Summary": f"- **Input**: {file}\n- **{param_info}**\n- **Output**: {output_path if 'output_path' in locals() else 'Parameter listing'}\n- **Format**: {format.upper()}"
                }
                
                git_logger.log_execution(
                    operation=operation,
                    parameters=parameters_dict,
                    results=results,
                    script_path=__file__,
                    additional_sections=additional_sections
                )
            except Exception as e:
                logger.error(f"Failed to create git log: {e}")
        
    except Exception as e:
        logger.error(f"Visualization error: {e}")
        click.echo(f"Error: {e}")
        _log_visualization_error_to_git(git_logger, "Visualization error", e, start_time, locals())
        sys.exit(1)


@cli.command()
@click.option('--file', '-f', required=True, help='CSV or JSON file with error data')
@click.option('--error-column', default='message', help='Column containing error data')
@click.option('--generate-graph', is_flag=True, help='Generate error frequency graphs')
@click.option('--nodes', help='Comma-separated list of node IDs to analyze')
@click.option('--output-dir', default='figures', help='Output directory for plots')
@click.option('--output-analysis', help='Save analysis results to JSON file')
@click.option('--no-git-log', is_flag=True, help='Disable automatic git logging')
@click.option('--note', help='Description for this error analysis')
@click.pass_context
def analyze_errors(ctx, file, error_column, generate_graph, nodes, output_dir, 
                  output_analysis, no_git_log, note):
    """Analyze error codes from GEMS sensor data files."""
    logger = ctx.obj['logger']
    
    # Initialize GitLogger
    git_logger = None
    if not no_git_log:
        try:
            git_logger = GitLogger(tool_name="error-analysis")
        except Exception as e:
            logger.warning(f"Failed to initialize git logging: {e}")
    
    start_time = datetime.now()
    
    try:
        # Import diagnostics modules
        from .diagnostics import ErrorCodeParser, parse_error_codes, analyze_error_patterns
        from .diagnostics.cli import load_data_file, filter_by_nodes, create_error_frequency_plot, setup_output_directory
        
        # Load data
        logger.info(f"Loading data from {file}")
        df = load_data_file(file)
        logger.info(f"Loaded {len(df)} records")
        
        # Parse node filter
        node_filter = []
        if nodes:
            node_filter = [n.strip() for n in nodes.split(',')]
        
        # Filter by nodes if specified
        if node_filter and 'all' not in node_filter:
            df = filter_by_nodes(df, node_filter)
            logger.info(f"Filtered to {len(df)} records for nodes: {node_filter}")
        
        # Parse error codes
        logger.info("Parsing error codes...")
        parser = ErrorCodeParser()
        parsed_errors_df = parser.parse_error_codes_from_data(df, error_column)
        
        if parsed_errors_df.empty:
            click.echo("No error codes found in the input file.")
            return
        
        logger.info(f"Parsed {len(parsed_errors_df)} error instances")
        
        # Analyze error patterns
        analysis = analyze_error_patterns(parsed_errors_df)
        
        # Print summary
        click.echo(f"\n=== ERROR ANALYSIS SUMMARY ===")
        click.echo(f"Total Errors: {analysis['total_errors']}")
        click.echo(f"Unique Error Codes: {analysis['unique_error_codes']}")
        click.echo(f"Date Range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
        
        # Print top error codes
        click.echo(f"\n=== TOP ERROR CODES ===")
        for i, error_info in enumerate(analysis['top_error_codes'], 1):
            click.echo(f"{i}. {error_info['code']} ({error_info['count']}): {error_info['description']}")
        
        # Print errors by device
        if 'errors_by_device' in analysis:
            click.echo(f"\n=== ERRORS BY DEVICE ===")
            for device, count in analysis['errors_by_device'].items():
                click.echo(f"  {device}: {count}")
        
        # Print errors by node
        if 'errors_by_node' in analysis:
            click.echo(f"\n=== ERRORS BY NODE ===")
            for node, count in list(analysis['errors_by_node'].items())[:10]:
                click.echo(f"  {node}: {count}")
            if len(analysis['errors_by_node']) > 10:
                click.echo(f"  ... and {len(analysis['errors_by_node']) - 10} more nodes")
        
        # Generate plots if requested
        output_dir_path = setup_output_directory(output_dir)
        plot_files = []
        
        if generate_graph:
            logger.info("Generating error frequency plots...")
            
            # Overall plot
            plot_file = create_error_frequency_plot(parsed_errors_df, output_dir_path, "all")
            if plot_file:
                plot_files.append(plot_file)
                click.echo(f"Error frequency plot saved to: {plot_file}")
            
            # Per-node plots if filtering by specific nodes
            if node_filter and 'all' not in node_filter:
                for node_id in node_filter:
                    node_errors = parsed_errors_df[parsed_errors_df['node_id'] == node_id]
                    if not node_errors.empty:
                        plot_file = create_error_frequency_plot(node_errors, output_dir_path, node_id)
                        if plot_file:
                            plot_files.append(plot_file)
                            click.echo(f"Node {node_id} plot saved to: {plot_file}")
        
        # Save analysis results if requested
        if output_analysis:
            with open(output_analysis, 'w') as f:
                import json
                json.dump(analysis, f, indent=2, default=str)
            click.echo(f"Analysis results saved to: {output_analysis}")
        
        # Create git log if enabled
        if git_logger:
            try:
                operation = f"Analyze error codes from {os.path.basename(file)}"
                if note:
                    operation += f" - {note}"
                
                parameters = {
                    'input_file': file,
                    'error_column': error_column,
                    'generate_graph': generate_graph,
                    'node_filter': node_filter,
                    'output_dir': output_dir,
                    'note': note
                }
                
                results = {
                    'success': True,
                    'total_errors_found': analysis['total_errors'],
                    'unique_error_codes': analysis['unique_error_codes'],
                    'plots_generated': len(plot_files),
                    'plot_files': plot_files,
                    'analysis_file': output_analysis,
                    'start_time': start_time.isoformat(),
                    'end_time': datetime.now().isoformat()
                }
                
                additional_sections = {
                    "Error Analysis Summary": f"- **Total Errors**: {analysis['total_errors']}\n- **Unique Codes**: {analysis['unique_error_codes']}\n- **Plots Generated**: {len(plot_files)}"
                }
                
                if plot_files:
                    additional_sections["Generated Plots"] = "\n".join([f"- {os.path.basename(p)}" for p in plot_files])
                
                git_logger.log_execution(
                    operation=operation,
                    parameters=parameters,
                    results=results,
                    script_path=__file__,
                    additional_sections=additional_sections
                )
            except Exception as e:
                logger.error(f"Failed to create git log: {e}")
        
    except Exception as e:
        logger.error(f"Error analysis failed: {e}")
        click.echo(f"Error: {e}")
        _log_error_analysis_error_to_git(git_logger, "Error analysis error", e, start_time, locals())
        sys.exit(1)


def _log_error_analysis_error_to_git(git_logger, error_type: str, error: Exception, start_time: datetime, local_vars: dict):
    """Helper function to log error analysis errors to git."""
    if not git_logger:
        return
    
    try:
        operation = f"Error analysis failed - {error_type}"
        
        # Extract parameters safely
        parameters = {}
        safe_vars = ['file', 'error_column', 'nodes', 'generate_graph', 'note']
        for var in safe_vars:
            if var in local_vars:
                parameters[var] = local_vars[var]
        
        results = {
            'success': False,
            'error': str(error),
            'error_type': error_type,
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat()
        }
        
        git_logger.log_execution(
            operation=operation,
            parameters=parameters,
            results=results,
            script_path=__file__
        )
    except Exception:
        # Don't let git logging errors crash the application
        pass


def setup_credentials_file():
    """Create template .env file with credentials."""
    env_path = Path.cwd() / '.env'
    
    # Check if .env already exists
    if env_path.exists():
        click.echo(f".env file already exists at {env_path}")
        if not click.confirm("Do you want to overwrite it?"):
            click.echo("Operation cancelled.")
            return
    
    # Create template content
    template_content = """# GEMS Database Configuration
# Update these values with your actual credentials

DB_HOST=sensing-0.msi.umn.edu
DB_PORT=5433
DB_NAME=gems
DB_USER=your_username
DB_PASSWORD=your_password

# Optional API Keys
PARTICLE_ACCESS_TOKEN=your_particle_token
CDS_API_KEY=your_cds_api_key
"""
    
    # Write template file
    with open(env_path, 'w') as f:
        f.write(template_content)
    
    click.echo(f"Created template .env file at {env_path}")
    click.echo("\nPlease edit this file and update the credentials:")
    click.echo("1. Replace 'your_username' with your database username")
    click.echo("2. Replace 'your_password' with your database password")
    click.echo("3. Ensure you are connected to the UMN VPN")
    click.echo("\nFor database access, contact the RTGS Lab.")


def list_projects_command(db_manager: DatabaseManager):
    """List available projects."""
    try:
        return list_projects(db_manager)
    except Exception as e:
        raise DatabaseError(f"Failed to list projects: {e}")


def _log_error_to_git(git_logger, error_type: str, error: Exception, start_time: datetime, local_vars: dict):
    """Helper function to log errors to git."""
    if not git_logger:
        return
    
    try:
        operation = f"Data extraction failed - {error_type}"
        
        # Extract parameters safely
        parameters = {}
        safe_vars = ['project', 'start_date', 'end_date', 'node_id', 'output', 'retry_count', 'note']
        for var in safe_vars:
            if var in local_vars:
                parameters[var] = local_vars[var]
        
        results = {
            'success': False,
            'error': str(error),
            'error_type': error_type,
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat()
        }
        
        git_logger.log_execution(
            operation=operation,
            parameters=parameters,
            results=results,
            script_path=__file__
        )
    except Exception as e:
        # Don't let git logging errors crash the application
        pass


def _log_era5_error_to_git(git_logger, error_type: str, error: Exception, start_time: datetime, local_vars: dict):
    """Helper function to log ERA5 errors to git."""
    if not git_logger:
        return
    
    try:
        operation = f"ERA5 download failed - {error_type}"
        
        # Extract parameters safely
        parameters = {}
        safe_vars = ['variables', 'start_date', 'end_date', 'area', 'output_file', 'pressure_levels', 'time_hours', 'note']
        for var in safe_vars:
            if var in local_vars:
                parameters[var] = local_vars[var]
        
        results = {
            'success': False,
            'error': str(error),
            'error_type': error_type,
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat()
        }
        
        git_logger.log_execution(
            operation=operation,
            parameters=parameters,
            results=results,
            script_path=__file__
        )
    except Exception as e:
        # Don't let git logging errors crash the application
        pass


def _log_visualization_error_to_git(git_logger, error_type: str, error: Exception, start_time: datetime, local_vars: dict):
    """Helper function to log visualization errors to git."""
    if not git_logger:
        return
    
    try:
        operation = f"Visualization failed - {error_type}"
        
        # Extract parameters safely
        parameters = {}
        safe_vars = ['file', 'parameter', 'node_id', 'multi_param', 'output_dir', 'format', 'title', 'note']
        for var in safe_vars:
            if var in local_vars:
                parameters[var] = local_vars[var]
        
        results = {
            'success': False,
            'error': str(error),
            'error_type': error_type,
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat()
        }
        
        git_logger.log_execution(
            operation=operation,
            parameters=parameters,
            results=results,
            script_path=__file__
        )
    except Exception as e:
        # Don't let git logging errors crash the application
        pass


if __name__ == '__main__':
    cli()