"""CLI module for error analysis tools."""

import json
import sys
from datetime import datetime
from pathlib import Path

import click

from ..core.cli_utils import (
    CLIContext, add_common_options, handle_common_errors
)


@click.group()
@click.pass_context
def error_analysis_cli(ctx):
    """Error analysis tools."""
    ctx.ensure_object(CLIContext)


@error_analysis_cli.command()
@click.option('--file', '-f', required=True, help='CSV or JSON file with error data')
@click.option('--error-column', default='message', help='Column containing error data')
@click.option('--generate-graph', is_flag=True, help='Generate error frequency graphs')
@click.option('--nodes', help='Comma-separated list of node IDs to analyze')
@click.option('--output-dir', default='figures', help='Output directory for plots')
@click.option('--output-analysis', help='Save analysis results to JSON file')
@add_common_options
@click.pass_context
@handle_common_errors("error-analysis")
def analyze(ctx, file, error_column, generate_graph, nodes, output_dir, 
           output_analysis, verbose, log_file, no_git_log, note):
    """Analyze error codes from GEMS sensor data files."""
    cli_ctx = ctx.obj
    cli_ctx.setup("error-analysis", verbose, log_file, no_git_log)
    
    try:
        from ..device_monitoring import ErrorCodeParser, parse_error_codes, analyze_error_patterns
        from ..device_monitoring.cli import load_data_file, filter_by_nodes, create_error_frequency_plot, setup_output_directory
        
        # Load data
        cli_ctx.logger.info(f"Loading data from {file}")
        df = load_data_file(file)
        cli_ctx.logger.info(f"Loaded {len(df)} records")
        
        # Parse node filter
        node_filter = []
        if nodes:
            node_filter = [n.strip() for n in nodes.split(',')]
        
        # Filter by nodes if specified
        if node_filter and 'all' not in node_filter:
            df = filter_by_nodes(df, node_filter)
            cli_ctx.logger.info(f"Filtered to {len(df)} records for nodes: {node_filter}")
        
        # Parse error codes
        cli_ctx.logger.info("Parsing error codes...")
        parser = ErrorCodeParser()
        parsed_errors_df = parser.parse_error_codes_from_data(df, error_column)
        
        if parsed_errors_df.empty:
            click.echo("No error codes found in the input file.")
            return
        
        cli_ctx.logger.info(f"Parsed {len(parsed_errors_df)} error instances")
        
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
            cli_ctx.logger.info("Generating error frequency plots...")
            
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
                json.dump(analysis, f, indent=2, default=str)
            click.echo(f"Analysis results saved to: {output_analysis}")
        
        # Log success to git
        operation = f"Analyze error codes from {Path(file).name}"
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
            'start_time': cli_ctx.start_time.isoformat(),
            'end_time': datetime.now().isoformat()
        }
        
        additional_sections = {
            "Error Analysis Summary": f"- **Total Errors**: {analysis['total_errors']}\n- **Unique Codes**: {analysis['unique_error_codes']}\n- **Plots Generated**: {len(plot_files)}"
        }
        
        if plot_files:
            additional_sections["Generated Plots"] = "\n".join([f"- {Path(p).name}" for p in plot_files])
        
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
            'input_file': file,
            'error_column': error_column,
            'generate_graph': generate_graph,
            'node_filter': nodes,
            'note': note
        }
        cli_ctx.log_error("Error analysis error", e, parameters, __file__)
        raise


@error_analysis_cli.command()
@click.argument('error_code')
@add_common_options
@click.pass_context
@handle_common_errors("error-decoding")
def decode(ctx, error_code, verbose, log_file, no_git_log, note):
    """Decode a single error code."""
    cli_ctx = ctx.obj
    cli_ctx.setup("error-decoding", verbose, log_file, no_git_log)
    
    try:
        from ..device_monitoring import ErrorCodeParser
        
        parser = ErrorCodeParser()
        parsed = parser.parse_error_code(error_code)
        
        click.echo(f"Error Code: {parsed['normalized_code']}")
        click.echo(f"Description: {parsed['full_description']}")
        click.echo(f"Error Class: {parsed['error_class_name']} ({parsed['error_class']})")
        click.echo(f"Hardware Device: {parsed['hardware_device_name']} ({parsed['hardware_device']})")
        click.echo(f"Sub-device: {parsed['hardware_sub_device_name']} ({parsed['hardware_sub_device']})")
        click.echo(f"Specific Code: {parsed['specific_error']}")
        
    except Exception as e:
        cli_ctx.log_error("Error decoding error", e, {'error_code': error_code, 'note': note}, __file__)
        raise


@error_analysis_cli.command()
@click.pass_context
def error_classes(ctx):
    """List all available error classes and hardware types."""
    from ..device_monitoring.error_parser import ERROR_CLASSES, HARDWARE_DEVICES, HARDWARE_SUB_DEVICES
    
    click.echo("=== ERROR CLASSES ===")
    for code, name in ERROR_CLASSES.items():
        click.echo(f"  {code}: {name}")
    
    click.echo("\n=== HARDWARE DEVICES ===")
    for code, name in HARDWARE_DEVICES.items():
        click.echo(f"  {code}: {name}")
    
    click.echo("\n=== HARDWARE SUB-DEVICES ===")
    for code, name in HARDWARE_SUB_DEVICES.items():
        click.echo(f"  {code}: {name}")


# Main command for external use
@click.command()
@click.option('--file', '-f', required=True, help='CSV or JSON file with error data')
@click.option('--error-column', default='message', help='Column containing error data')
@click.option('--generate-graph', is_flag=True, help='Generate error frequency graphs')
@click.option('--nodes', help='Comma-separated list of node IDs to analyze')
@click.option('--output-dir', default='figures', help='Output directory for plots')
@click.option('--output-analysis', help='Save analysis results to JSON file')
@add_common_options
def analyze_errors_command(**kwargs):
    """Analyze error codes from GEMS sensor data files."""
    # Create a context and invoke the analyze command
    ctx = click.Context(analyze)
    ctx.obj = CLIContext()
    ctx.invoke(analyze, **kwargs)


if __name__ == '__main__':
    error_analysis_cli()