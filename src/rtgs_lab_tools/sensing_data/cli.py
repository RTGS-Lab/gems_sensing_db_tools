"""CLI module for sensing data extraction tools."""

import sys
from datetime import datetime
from pathlib import Path

import click
import pandas as pd

from ..core import Config, DatabaseManager
from ..core.cli_utils import (
    CLIContext, add_common_options, handle_common_errors,
    validate_date_format, parse_node_ids, create_setup_credentials_command
)
from ..core.exceptions import DatabaseError
from ..sensing_data import get_raw_data, list_projects, save_data, create_zip_archive
from ..sensing_data.file_operations import ensure_data_directory


@click.group()
@click.pass_context
def sensing_data_cli(ctx):
    """Sensing data extraction tools."""
    ctx.ensure_object(CLIContext)


@sensing_data_cli.command()
@click.option('--project', '-p', help='Project name to query')
@click.option('--list-projects', is_flag=True, help='List all available projects and exit')
@click.option('--setup-credentials', is_flag=True, help='Create template .env file')
@click.option('--start-date', default="2018-01-01", help='Start date (YYYY-MM-DD)')
@click.option('--end-date', help='End date (YYYY-MM-DD), defaults to today')
@click.option('--node-id', help='Comma-separated list of node IDs to query')
@click.option('--output-dir', help='Output directory for data files (default: ./data)')
@click.option('--output', type=click.Choice(['csv', 'parquet']), default='csv', help='Output format')
@click.option('--create-zip', is_flag=True, help='Create zip archive with metadata')
@click.option('--retry-count', type=int, default=3, help='Maximum retry attempts')
@add_common_options
@click.pass_context
@handle_common_errors("data-extraction")
def extract(ctx, project, list_projects, setup_credentials, start_date, end_date, 
           node_id, output_dir, output, create_zip, retry_count, verbose, log_file, 
           no_git_log, note):
    """Extract sensing data from GEMS database."""
    cli_ctx = ctx.obj
    cli_ctx.setup("data-extraction", verbose, log_file, no_git_log)
    
    # Handle setup credentials
    if setup_credentials:
        setup_creds_cmd = create_setup_credentials_command()
        ctx.invoke(setup_creds_cmd)
        return
    
    # Initialize configuration and database
    config = Config()
    db_manager = DatabaseManager(config)
    
    # Test database connection
    if not db_manager.test_connection():
        cli_ctx.logger.error("Failed to connect to database. Please check your configuration and VPN connection.")
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
    
    # Validate dates
    validate_date_format(start_date, "start-date")
    if end_date:
        validate_date_format(end_date, "end-date")
    else:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    # Parse node IDs
    node_ids = parse_node_ids(node_id)
    
    # Ensure output directory
    output_directory = ensure_data_directory(output_dir)
    
    try:
        # Extract data
        cli_ctx.logger.info(f"Extracting data for project: {project}")
        df = get_raw_data(
            database_manager=db_manager,
            project=project,
            start_date=start_date,
            end_date=end_date,
            node_ids=node_ids,
            max_retries=retry_count
        )
        
        if df.empty:
            cli_ctx.logger.info("No data found for the specified parameters")
            return
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project.replace(' ', '_')}_{start_date}_to_{end_date}_{timestamp}"
        
        # Save data
        file_path = save_data(df, output_directory, filename, output)
        
        # Create zip archive if requested
        zip_path = None
        if create_zip:
            zip_path = create_zip_archive(file_path, df, output)
            click.echo(f"Created zip archive: {zip_path}")
        else:
            click.echo(f"Data saved to: {file_path}")
        
        # Print summary
        click.echo(f"Successfully extracted {len(df)} records")
        
        # Log success to git
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
            'start_time': cli_ctx.start_time.isoformat(),
            'end_time': datetime.now().isoformat()
        }
        
        additional_sections = {
            "Data Summary": f"- **Records**: {len(df)}\n- **Output**: {file_path}\n- **Format**: {output.upper()}"
        }
        
        if create_zip:
            additional_sections["Archive"] = f"- **Zip Archive**: {zip_path}"
        
        cli_ctx.log_success(
            operation=operation,
            parameters=parameters,
            results=results,
            script_path=__file__,
            additional_sections=additional_sections
        )
        
    except Exception as e:
        # Log error
        parameters = {
            'project': project,
            'start_date': start_date,
            'end_date': end_date,
            'node_ids': node_ids,
            'output_format': output,
            'retry_count': retry_count,
            'note': note
        }
        cli_ctx.log_error("Data extraction error", e, parameters, __file__)
        raise
    
    finally:
        db_manager.close()


@sensing_data_cli.command()
@add_common_options
@click.pass_context
@handle_common_errors("project-listing")
def list_projects_cmd(ctx, verbose, log_file, no_git_log, note):
    """List all available projects in the database."""
    cli_ctx = ctx.obj
    cli_ctx.setup("project-listing", verbose, log_file, no_git_log)
    
    config = Config()
    db_manager = DatabaseManager(config)
    
    if not db_manager.test_connection():
        cli_ctx.logger.error("Failed to connect to database.")
        sys.exit(1)
    
    try:
        projects = list_projects_command(db_manager)
        if projects:
            click.echo("Available projects:")
            for project_name, node_count in projects:
                click.echo(f"  {project_name} ({node_count} nodes)")
        else:
            click.echo("No projects found.")
            
    finally:
        db_manager.close()


def list_projects_command(db_manager: DatabaseManager):
    """List available projects."""
    try:
        return list_projects(db_manager)
    except Exception as e:
        raise DatabaseError(f"Failed to list projects: {e}")


# Main command for external use
@click.command()
@click.option('--project', '-p', help='Project name to query')
@click.option('--list-projects', is_flag=True, help='List all available projects and exit')
@click.option('--setup-credentials', is_flag=True, help='Create template .env file')
@click.option('--start-date', default="2018-01-01", help='Start date (YYYY-MM-DD)')
@click.option('--end-date', help='End date (YYYY-MM-DD), defaults to today')
@click.option('--node-id', help='Comma-separated list of node IDs to query')
@click.option('--output-dir', help='Output directory for data files (default: ./data)')
@click.option('--output', type=click.Choice(['csv', 'parquet']), default='csv', help='Output format')
@click.option('--create-zip', is_flag=True, help='Create zip archive with metadata')
@click.option('--retry-count', type=int, default=3, help='Maximum retry attempts')
@add_common_options
def data_command(**kwargs):
    """Extract sensing data from GEMS database."""
    # Create a context and invoke the extract command
    ctx = click.Context(extract)
    ctx.obj = CLIContext()
    ctx.invoke(extract, **kwargs)


if __name__ == '__main__':
    sensing_data_cli()