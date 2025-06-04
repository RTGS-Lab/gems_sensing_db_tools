"""Main CLI router for RTGS Lab Tools."""

import click


@click.group()
def cli():
    """RTGS Lab Tools - Environmental sensing and climate data toolkit."""
    pass


# Import and add the individual tool commands directly
def register_commands():
    """Register all tool commands with the main CLI."""
    
    # Import the actual command functions from each tool
    from .sensing_data.cli import data_command
    from .visualization.cli import visualize_command
    from .gridded_data.cli import era5_command
    from .device_configuration.cli import device_config_command
    from .device_monitoring.cli import analyze_errors_command
    
    # Add them to the main CLI with their specific names
    cli.add_command(data_command, name='data')
    cli.add_command(visualize_command, name='visualize')
    cli.add_command(era5_command, name='era5')
    cli.add_command(device_config_command, name='device-config')
    cli.add_command(analyze_errors_command, name='analyze-errors')


# Register commands when the module is imported
register_commands()


if __name__ == '__main__':
    cli()