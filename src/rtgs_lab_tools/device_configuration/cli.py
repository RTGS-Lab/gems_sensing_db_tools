"""CLI module for device configuration management tools."""

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
def device_config_cli(ctx):
    """Device configuration management tools."""
    ctx.ensure_object(CLIContext)


@device_config_cli.command()
@click.option('--config', required=True, help='Configuration as JSON string OR path to configuration file')
@click.option('--devices', required=True, help='Device IDs as comma-separated string OR path to device list file')
@click.option('--max-retries', type=int, default=3, help='Maximum retry attempts per device')
@click.option('--restart-wait', type=int, default=30, help='Seconds to wait for device restart')
@click.option('--online-timeout', type=int, default=120, help='Seconds to wait for device to come online')
@click.option('--max-concurrent', type=int, default=5, help='Maximum concurrent devices to process')
@click.option('--dry-run', is_flag=True, help='Validate inputs without making changes')
@click.option('--output-file', default='update_results.json', help='Output file for detailed results')
@add_common_options
@click.pass_context
@handle_common_errors("device-configuration")
def update(ctx, config, devices, max_retries, restart_wait, online_timeout, 
          max_concurrent, dry_run, output_file, verbose, log_file, no_git_log, note):
    """Update sensor and system configuration on multiple Particle devices."""
    cli_ctx = ctx.obj
    cli_ctx.setup("device-configuration", verbose, log_file, no_git_log)
    
    try:
        from ..device_configuration import ParticleClient, ConfigurationManager, DeviceConfigurationUpdater
        
        # Initialize components
        particle_client = ParticleClient()
        config_manager = ConfigurationManager()
        updater = DeviceConfigurationUpdater(particle_client, config_manager)
        
        # Load configuration
        if Path(config).exists():
            configuration = config_manager.load_configurations(config)
        else:
            try:
                configuration = json.loads(config)
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON configuration: {e}")
                sys.exit(1)
        
        # Validate configuration
        config_manager.validate_configuration(configuration)
        
        # Load device list
        if Path(devices).exists():
            device_ids = updater.load_device_list(devices)
        else:
            device_ids = [d.strip() for d in devices.split(',') if d.strip()]
        
        if not device_ids:
            click.echo("Error: No devices specified")
            sys.exit(1)
        
        cli_ctx.logger.info(f"Starting update for {len(device_ids)} devices")
        if dry_run:
            cli_ctx.logger.info("DRY RUN MODE - No actual changes will be made")
        
        # Update devices
        summary = updater.update_multiple_devices(
            device_ids=device_ids,
            configuration=configuration,
            max_workers=max_concurrent,
            verify=not dry_run  # Skip verification in dry run
        )
        
        # Save results to file
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        click.echo(f"\n=== UPDATE SUMMARY ===")
        click.echo(f"Total Devices: {summary['total_devices']}")
        click.echo(f"Successful: {summary['successful']}")
        click.echo(f"Failed: {summary['failed']}")
        if 'verification_failed' in summary:
            click.echo(f"Verification Failed: {summary['verification_failed']}")
        click.echo(f"Results saved to: {output_file}")
        
        # Log success to git
        operation = f"Update configuration on {len(device_ids)} devices"
        if note:
            operation += f" - {note}"
        
        parameters = {
            'config_source': config,
            'device_source': devices,
            'device_count': len(device_ids),
            'max_retries': max_retries,
            'restart_wait': restart_wait,
            'online_timeout': online_timeout,
            'max_concurrent': max_concurrent,
            'dry_run': dry_run,
            'output_file': output_file,
            'note': note
        }
        
        results = {
            'success': True,
            'total_devices': summary['total_devices'],
            'successful_devices': summary['successful'],
            'failed_devices': summary['failed'],
            'success_rate': f"{(summary['successful'] / summary['total_devices'] * 100):.1f}%" if summary['total_devices'] > 0 else "0%",
            'output_file': output_file,
            'dry_run': dry_run,
            'start_time': cli_ctx.start_time.isoformat(),
            'end_time': datetime.now().isoformat()
        }
        
        # Format device results for display
        device_results = []
        for device_result in summary.get('results', {}).values():
            status = "✅" if device_result.get('status') in ['completed', 'verified'] else "❌"
            device_id = device_result['device_id']
            
            if device_result.get('status') in ['completed', 'verified']:
                system_uid = device_result.get('system_uid', 'N/A')
                sensor_uid = device_result.get('sensor_uid', 'N/A')
                device_results.append(f"- {status} `{device_id}` - Success (System UID: {system_uid}, Sensor UID: {sensor_uid})")
            else:
                error = device_result.get('error', 'Unknown error')
                device_results.append(f"- {status} `{device_id}` - Failed: {error}")
        
        additional_sections = {
            "Configuration Applied": f"```json\n{json.dumps(configuration, indent=2)}\n```",
            "Device Results": "\n".join(device_results[:20])  # Limit to first 20 for readability
        }
        
        if len(device_results) > 20:
            additional_sections["Device Results"] += f"\n... and {len(device_results) - 20} more devices"
        
        cli_ctx.log_success(
            operation=operation,
            parameters=parameters,
            results=results,
            script_path=__file__,
            additional_sections=additional_sections
        )
        
        # Exit with appropriate code
        if summary['failed'] > 0:
            cli_ctx.logger.error(f"Some devices failed to update: {summary['failed']}/{summary['total_devices']}")
            sys.exit(1)
        else:
            cli_ctx.logger.info("All devices updated successfully")
        
    except Exception as e:
        # Log error
        parameters = {
            'config_source': config,
            'device_source': devices,
            'max_retries': max_retries,
            'dry_run': dry_run,
            'note': note
        }
        cli_ctx.log_error("Device configuration error", e, parameters, __file__)
        raise


@device_config_cli.command()
@click.pass_context
def create_template(ctx):
    """Create a template configuration for Particle devices."""
    template_config = {
        "config": {
            "system": {
                "logPeriod": 300,
                "backhaulCount": 4,
                "powerSaveMode": 1,
                "loggingMode": 0,
                "numAuxTalons": 1,
                "numI2CTalons": 1,
                "numSDI12Talons": 1
            },
            "sensors": {
                "numET": 0,
                "numHaar": 0,
                "numSoil": 3,
                "numApogeeSolar": 0,
                "numCO2": 0,
                "numO2": 0,
                "numPressure": 0
            }
        }
    }
    
    click.echo("Template configuration for Particle devices:")
    click.echo(json.dumps(template_config, indent=2))
    click.echo("\nSave this to a file and modify as needed before applying.")
    click.echo("Use the 'update' command with --config pointing to your configuration file.")


@device_config_cli.command()
@add_common_options
@click.pass_context
@handle_common_errors("device-listing")
def list_devices(ctx, verbose, log_file, no_git_log, note):
    """List all Particle devices in the account."""
    cli_ctx = ctx.obj
    cli_ctx.setup("device-listing", verbose, log_file, no_git_log)
    
    try:
        from ..device_configuration import ParticleClient
        
        client = ParticleClient()
        devices = client.list_devices()
        
        if not devices:
            click.echo("No devices found.")
            return
        
        click.echo(f"Found {len(devices)} devices:")
        for device in devices:
            online_status = "🟢 online" if device.get('connected') else "🔴 offline"
            device_name = device.get('name', 'unnamed')
            device_id = device.get('id', 'unknown')
            platform = device.get('platform_id', 'unknown')
            
            click.echo(f"  {online_status} {device_name} ({device_id}) - Platform: {platform}")
            
    except Exception as e:
        cli_ctx.log_error("Device listing error", e, {'note': note}, __file__)
        raise


# Main command for external use
@click.command()
@click.option('--config', required=True, help='Configuration as JSON string OR path to configuration file')
@click.option('--devices', required=True, help='Device IDs as comma-separated string OR path to device list file')
@click.option('--max-retries', type=int, default=3, help='Maximum retry attempts per device')
@click.option('--restart-wait', type=int, default=30, help='Seconds to wait for device restart')
@click.option('--online-timeout', type=int, default=120, help='Seconds to wait for device to come online')
@click.option('--max-concurrent', type=int, default=5, help='Maximum concurrent devices to process')
@click.option('--dry-run', is_flag=True, help='Validate inputs without making changes')
@click.option('--output-file', default='update_results.json', help='Output file for detailed results')
@add_common_options
def device_config_command(**kwargs):
    """Update sensor and system configuration on multiple Particle devices."""
    # Create a context and invoke the update command
    ctx = click.Context(update)
    ctx.obj = CLIContext()
    ctx.invoke(update, **kwargs)


if __name__ == '__main__':
    device_config_cli()