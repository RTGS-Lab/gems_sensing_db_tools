"""Shared CLI utilities for RTGS Lab Tools."""

import logging
import sys
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Optional

import click

from . import setup_logging, GitLogger
from .exceptions import RTGSLabToolsError, DatabaseError, ConfigError, APIError, ValidationError


def setup_logging_for_tool(tool_name: str, verbose: bool = False, log_file: Optional[str] = None) -> logging.Logger:
    """Set up logging for a specific tool.
    
    Args:
        tool_name: Name of the tool for logger naming
        verbose: Enable verbose (DEBUG) logging
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    log_level = "DEBUG" if verbose else "INFO"
    logger = setup_logging(log_level, log_file=log_file)
    return logger


def setup_git_logger(tool_name: str, disable: bool = False) -> Optional[GitLogger]:
    """Set up git logger for a specific tool.
    
    Args:
        tool_name: Name of the tool for git logging
        disable: Whether to disable git logging
        
    Returns:
        GitLogger instance or None if disabled/failed
    """
    if disable:
        return None
    
    try:
        return GitLogger(tool_name=tool_name)
    except Exception as e:
        # Log warning but don't fail the tool
        logging.getLogger().warning(f"Failed to initialize git logging for {tool_name}: {e}")
        return None


def log_error_to_git(
    git_logger: Optional[GitLogger], 
    error_type: str, 
    error: Exception, 
    start_time: datetime, 
    parameters: Dict[str, Any],
    script_path: str
):
    """Helper function to log errors to git.
    
    Args:
        git_logger: GitLogger instance (can be None)
        error_type: Type/category of error
        error: The exception that occurred
        start_time: When the operation started
        parameters: Parameters passed to the operation
        script_path: Path to the script being executed
    """
    if not git_logger:
        return
    
    try:
        operation = f"Operation failed - {error_type}"
        
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
            script_path=script_path
        )
    except Exception:
        # Don't let git logging errors crash the application
        pass


def handle_common_errors(tool_name: str):
    """Decorator to handle common errors across all CLI tools.
    
    Args:
        tool_name: Name of the tool for error context
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConfigError as e:
                click.echo(f"Configuration error: {e}", err=True)
                click.echo("Run with --setup-credentials to create a template .env file", err=True)
                sys.exit(1)
            except DatabaseError as e:
                click.echo(f"Database error: {e}", err=True)
                click.echo("Ensure you are connected to the UMN VPN and have valid credentials", err=True)
                sys.exit(1)
            except APIError as e:
                click.echo(f"API error: {e}", err=True)
                sys.exit(1)
            except ValidationError as e:
                click.echo(f"Validation error: {e}", err=True)
                sys.exit(1)
            except RTGSLabToolsError as e:
                click.echo(f"Error: {e}", err=True)
                sys.exit(1)
            except Exception as e:
                click.echo(f"Unexpected error in {tool_name}: {e}", err=True)
                sys.exit(1)
        return wrapper
    return decorator


def add_common_options(func: Callable) -> Callable:
    """Add common CLI options to a command.
    
    Args:
        func: Click command function to decorate
        
    Returns:
        Decorated function with common options
    """
    # Add options in reverse order due to how decorators work
    func = click.option('--no-git-log', is_flag=True, help='Disable automatic git logging')(func)
    func = click.option('--note', help='Note describing the purpose of this operation')(func)
    func = click.option('--log-file', help='Log to file')(func)
    func = click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')(func)
    return func


def create_setup_credentials_command():
    """Create the setup-credentials command that can be reused."""
    @click.command()
    def setup_credentials():
        """Create template .env file with credentials."""
        from pathlib import Path
        
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
    
    return setup_credentials


def validate_date_format(date_str: str, param_name: str) -> str:
    """Validate date format and return normalized date string.
    
    Args:
        date_str: Date string to validate
        param_name: Parameter name for error messages
        
    Returns:
        Validated date string
        
    Raises:
        ValidationError: If date format is invalid
    """
    try:
        # Try parsing the date
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValidationError(f"Invalid {param_name} format. Use YYYY-MM-DD (e.g., 2023-01-01)")


def parse_node_ids(node_id_str: Optional[str]) -> Optional[list]:
    """Parse comma-separated node IDs.
    
    Args:
        node_id_str: Comma-separated node ID string
        
    Returns:
        List of node IDs or None
    """
    if not node_id_str:
        return None
    
    return [n.strip() for n in node_id_str.split(',') if n.strip()]


def parse_area_bounds(area_str: str) -> list:
    """Parse area bounds string into list of floats.
    
    Args:
        area_str: Area bounds as "north,west,south,east"
        
    Returns:
        List of [north, west, south, east] floats
        
    Raises:
        ValidationError: If area format is invalid
    """
    try:
        bounds = [float(x.strip()) for x in area_str.split(',')]
        if len(bounds) != 4:
            raise ValueError()
        return bounds
    except ValueError:
        raise ValidationError("Area must be 'north,west,south,east' (4 comma-separated numbers)")


def parse_comma_separated_list(list_str: str, item_type: type = str, item_name: str = "items") -> list:
    """Parse comma-separated list with type conversion.
    
    Args:
        list_str: Comma-separated string
        item_type: Type to convert items to
        item_name: Name for error messages
        
    Returns:
        List of converted items
        
    Raises:
        ValidationError: If conversion fails
    """
    try:
        return [item_type(x.strip()) for x in list_str.split(',') if x.strip()]
    except ValueError as e:
        raise ValidationError(f"Invalid {item_name} format: {e}")


# Context class for passing data between CLI commands
class CLIContext:
    """Context object for sharing data between CLI commands."""
    
    def __init__(self):
        self.logger: Optional[logging.Logger] = None
        self.git_logger: Optional[GitLogger] = None
        self.start_time: Optional[datetime] = None
        self.tool_name: Optional[str] = None
    
    def setup(self, tool_name: str, verbose: bool = False, log_file: Optional[str] = None, no_git_log: bool = False):
        """Set up context for a tool.
        
        Args:
            tool_name: Name of the tool
            verbose: Enable verbose logging
            log_file: Optional log file
            no_git_log: Disable git logging
        """
        self.tool_name = tool_name
        self.logger = setup_logging_for_tool(tool_name, verbose, log_file)
        self.git_logger = setup_git_logger(tool_name, no_git_log)
        self.start_time = datetime.now()
    
    def log_error(self, error_type: str, error: Exception, parameters: Dict[str, Any], script_path: str):
        """Log error to git if git logger is available."""
        if self.git_logger and self.start_time:
            log_error_to_git(
                self.git_logger,
                error_type,
                error,
                self.start_time,
                parameters,
                script_path
            )
    
    def log_success(self, operation: str, parameters: Dict[str, Any], results: Dict[str, Any], 
                   script_path: str, additional_sections: Optional[Dict[str, str]] = None):
        """Log successful operation to git if git logger is available."""
        if self.git_logger:
            try:
                self.git_logger.log_execution(
                    operation=operation,
                    parameters=parameters,
                    results=results,
                    script_path=script_path,
                    additional_sections=additional_sections
                )
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Failed to create git log: {e}")