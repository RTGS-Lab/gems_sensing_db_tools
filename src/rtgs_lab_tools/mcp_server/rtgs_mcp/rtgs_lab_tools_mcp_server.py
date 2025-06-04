"""FastMCP server for RTGS Lab Tools - Natural language interface to all tools."""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("rtgs-lab-tools")

# Get the absolute path to the Python executable
PYTHON_EXECUTABLE = sys.executable

# Get the root directory of the project
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
RTGS_CLI_PATH = PROJECT_ROOT / "src" / "rtgs_lab_tools" / "cli.py"

# Original script paths for backward compatibility
DEVICE_CONFIG_UPDATER_PATH = PROJECT_ROOT / "src" / "rtgs_lab_tools" / "device_management" / "device_config_updater.py"


# -----------------
# DATA EXTRACTION TOOLS
# -----------------

@mcp.tool("extract_sensing_data")
async def extract_sensing_data(
    project: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    node_ids: Optional[str] = None,
    output_format: str = "csv",
    create_zip: bool = False,
    output_dir: Optional[str] = None,
    note: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract raw sensor data from the GEMS Sensing database with automatic git logging.
    
    Args:
        project: Project name to query (required)
        start_date: Start date in YYYY-MM-DD format (default: 2018-01-01)
        end_date: End date in YYYY-MM-DD format (default: today)
        node_ids: Comma-separated list of node IDs to query (optional)
        output_format: Output format - "csv" or "parquet" (default: csv)
        create_zip: Create a zip archive with metadata (default: False)
        output_dir: Custom output directory (default: ./data)
        note: Description for this data extraction (optional)
    """
    try:
        # Set MCP environment variables for proper git logging
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        # Build command to call the CLI
        cmd = [
            PYTHON_EXECUTABLE, str(RTGS_CLI_PATH), "data",
            "--project", project,
            "--output", output_format
        ]
        
        if start_date:
            cmd.extend(["--start-date", start_date])
        
        if end_date:
            cmd.extend(["--end-date", end_date])
        
        if node_ids:
            cmd.extend(["--node-id", node_ids])
        
        if create_zip:
            cmd.append("--create-zip")
        
        if output_dir:
            cmd.extend(["--output-dir", output_dir])
        
        if note:
            cmd.extend(["--note", note])
        
        # Run with MCP environment for proper git logging
        stdout, stderr = await run_command_with_env(cmd, env)
        
        return {
            "success": True,
            "output": stdout,
            "stderr": stderr if stderr else None,
            "command": " ".join(cmd),
            "mcp_execution": True,
            "git_logging_enabled": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Data extraction failed: {str(e)}",
            "command": " ".join(cmd) if 'cmd' in locals() else "N/A",
            "mcp_execution": True
        }


@mcp.tool("list_available_projects")
async def list_available_projects() -> Dict[str, Any]:
    """List all available projects in the GEMS Sensing database."""
    try:
        # Set MCP environment variables
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, str(RTGS_CLI_PATH), "data", "--list-projects"]
        
        stdout, stderr = await run_command_with_env(cmd, env)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list projects: {str(e)}"
        }


# -----------------
# VISUALIZATION TOOLS
# -----------------

@mcp.tool("create_visualization")
async def create_visualization(
    file_path: str,
    parameter: Optional[str] = None,
    node_id: Optional[str] = None,
    multi_param: Optional[List[str]] = None,
    output_file: Optional[str] = None,
    format: str = "png",
    title: Optional[str] = None,
    note: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create visualizations from sensor data with automatic git logging.
    
    Args:
        file_path: Path to the CSV file containing sensor data
        parameter: Parameter path to plot (e.g., "Data.Devices.0.Temperature")
        node_id: Specific node ID to plot
        multi_param: List of parameters as "node_id,parameter_path" for multi-parameter plots
        output_file: Output filename (without extension)
        format: Output format (png, pdf, svg) (default: png)
        title: Plot title (optional)
        note: Description for this visualization (optional)
    """
    try:
        # Set MCP environment variables
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, str(RTGS_CLI_PATH), "visualize", "--file", file_path, "--format", format]
        
        if parameter:
            cmd.extend(["--parameter", parameter])
        
        if node_id:
            cmd.extend(["--node-id", node_id])
        
        if multi_param:
            for param in multi_param:
                cmd.extend(["--multi-param", param])
        
        if output_file:
            cmd.extend(["--output-file", output_file])
        
        if title:
            cmd.extend(["--title", title])
        
        if note:
            cmd.extend(["--note", note])
        
        stdout, stderr = await run_command_with_env(cmd, env)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd),
            "mcp_execution": True,
            "git_logging_enabled": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Visualization failed: {str(e)}",
            "command": " ".join(cmd) if 'cmd' in locals() else "N/A"
        }


@mcp.tool("list_available_parameters")
async def list_available_parameters(file_path: str) -> Dict[str, Any]:
    """List available parameters in a sensor data file."""
    try:
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, str(RTGS_CLI_PATH), "visualize", "--file", file_path, "--list-params"]
        
        stdout, stderr = await run_command_with_env(cmd, env)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list parameters: {str(e)}"
        }


# -----------------
# ERA5 CLIMATE DATA TOOLS
# -----------------

@mcp.tool("download_era5_data")
async def download_era5_data(
    variables: List[str],
    start_date: str,
    end_date: str,
    area: Optional[str] = None,
    output_file: Optional[str] = None,
    pressure_levels: Optional[str] = None,
    time_hours: Optional[str] = None,
    process: bool = False,
    note: Optional[str] = None
) -> Dict[str, Any]:
    """
    Download ERA5 climate reanalysis data with automatic git logging.
    
    Args:
        variables: List of ERA5 variables to download
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        area: Bounding box as "north,west,south,east" (optional)
        output_file: Output NetCDF file path (optional)
        pressure_levels: Pressure levels as comma-separated values (optional)
        time_hours: Specific hours as comma-separated values (optional)
        process: Process downloaded data for basic statistics (default: False)
        note: Description for this download (optional)
    """
    try:
        # Set MCP environment variables
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, str(RTGS_CLI_PATH), "era5", "--start-date", start_date, "--end-date", end_date]
        
        # Add variables
        for var in variables:
            cmd.extend(["--variables", var])
        
        if area:
            cmd.extend(["--area", area])
        
        if output_file:
            cmd.extend(["--output-file", output_file])
        
        if pressure_levels:
            cmd.extend(["--pressure-levels", pressure_levels])
        
        if time_hours:
            cmd.extend(["--time-hours", time_hours])
        
        if process:
            cmd.append("--process")
        
        if note:
            cmd.extend(["--note", note])
        
        stdout, stderr = await run_command_with_env(cmd, env)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd),
            "mcp_execution": True,
            "git_logging_enabled": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"ERA5 download failed: {str(e)}",
            "command": " ".join(cmd) if 'cmd' in locals() else "N/A"
        }


@mcp.tool("list_era5_variables")
async def list_era5_variables() -> Dict[str, Any]:
    """List available ERA5 variables."""
    try:
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, str(RTGS_CLI_PATH), "era5", "--list-variables", "--variables", "placeholder"]
        
        stdout, stderr = await run_command_with_env(cmd, env)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list ERA5 variables: {str(e)}"
        }


# -----------------
# DEVICE MANAGEMENT TOOLS
# -----------------

@mcp.tool("update_particle_device_configurations")
async def update_particle_device_configurations(
    config: str,
    devices: str,
    max_retries: int = 3,
    restart_wait: int = 30,
    online_timeout: int = 120,
    max_concurrent: int = 5,
    dry_run: bool = False,
    output_file: str = "update_results.json",
    note: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update sensor and system configuration on multiple Particle devices with automatic git logging.
    This tool calls the original device configuration updater to maintain full functionality.
    
    Args:
        config: Configuration as JSON string OR path to configuration file
        devices: Device IDs as comma-separated string OR path to device list file
        max_retries: Maximum retry attempts per device (default: 3)
        restart_wait: Seconds to wait for device restart (default: 30)
        online_timeout: Seconds to wait for device to come online (default: 120)
        max_concurrent: Maximum concurrent devices to process (default: 5)
        dry_run: Validate inputs without making changes (default: False)
        output_file: Output file for detailed results (default: update_results.json)
        note: Description for this configuration update (optional)
    """
    try:
        # Set MCP environment variables for proper git logging
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        # Use the original script to maintain all functionality and git logging
        cmd = [
            PYTHON_EXECUTABLE, str(ORIGINAL_DEVICE_UPDATER_PATH),
            "--config", config,
            "--devices", devices,
            "--output", output_file,
            "--max-retries", str(max_retries),
            "--restart-wait", str(restart_wait),
            "--online-timeout", str(online_timeout),
            "--max-concurrent", str(max_concurrent)
        ]
        
        if dry_run:
            cmd.append("--dry-run")
        
        if note:
            cmd.extend(["--note", note])
        
        # Run with MCP environment for proper logging
        stdout, stderr = await run_command_with_env(cmd, env)
        
        # Try to load and parse the results file if it exists
        results_data = None
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r') as f:
                    results_data = json.load(f)
            except Exception:
                pass  # Continue without results data if parsing fails
        
        result = {
            "success": True,
            "output": stdout,
            "stderr": stderr if stderr else None,
            "command": " ".join(cmd),
            "results_file": output_file,
            "mcp_execution": True,
            "git_logging_enabled": True,
            "dry_run": dry_run
        }
        
        # Add parsed results if available
        if results_data:
            result["summary"] = results_data.get("summary", {})
            result["device_count"] = results_data["summary"].get("total_devices", 0)
            result["successful_count"] = results_data["summary"].get("successful", 0)
            result["failed_count"] = results_data["summary"].get("failed", 0)
            
            if not dry_run and result["device_count"] > 0:
                success_rate = (result["successful_count"] / result["device_count"] * 100)
                result["success_rate"] = f"{success_rate:.1f}%"
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Configuration update failed: {str(e)}",
            "command": " ".join(cmd) if 'cmd' in locals() else "N/A",
            "mcp_execution": True
        }


@mcp.tool("create_device_config_template")
async def create_device_config_template() -> Dict[str, Any]:
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
    
    return {
        "success": True,
        "config_template": template_config,
        "config_string": json.dumps(template_config),
        "description": "Template configuration for Particle devices. Modify values as needed before applying.",
        "usage": "Pass the config_string as the 'config' parameter to update_particle_device_configurations"
    }


# -----------------
# ERROR ANALYSIS TOOLS
# -----------------

@mcp.tool("analyze_error_codes")
async def analyze_error_codes(
    file_path: str,
    generate_graph: bool = False,
    node_filter: Optional[str] = None,
    error_column: str = "message",
    output_analysis: Optional[str] = None,
    note: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse and analyze error codes from GEMS sensor data files with automatic git logging.
    
    Args:
        file_path: Path to the CSV or JSON file containing error data
        generate_graph: Whether to generate error frequency graphs (default: False)
        node_filter: Comma-separated list of node IDs to filter errors by (use "all" to separate by node)
        error_column: Column containing error data (default: "message")
        output_analysis: Save analysis results to JSON file (optional)
        note: Description for this error analysis (optional)
    """
    try:
        # Set MCP environment variables
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        # Call the new CLI error analysis command
        cmd = [PYTHON_EXECUTABLE, str(RTGS_CLI_PATH), "analyze-errors", "--file", file_path, "--error-column", error_column]
        
        if generate_graph:
            cmd.append("--generate-graph")
        
        if node_filter:
            cmd.extend(["--nodes", node_filter])
        
        if output_analysis:
            cmd.extend(["--output-analysis", output_analysis])
        
        if note:
            cmd.extend(["--note", note])
        
        stdout, stderr = await run_command_with_env(cmd, env)
        
        # Determine output files from stdout
        graph_files = []
        if generate_graph:
            for line in stdout.splitlines():
                if "plot saved to:" in line:
                    graph_file = line.split("plot saved to:")[1].strip()
                    if os.path.exists(graph_file):
                        graph_files.append(graph_file)
        
        result = {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd),
            "mcp_execution": True,
            "git_logging_enabled": True
        }
        
        if graph_files:
            result["graph_files"] = graph_files
        
        if output_analysis and os.path.exists(output_analysis):
            result["analysis_file"] = output_analysis
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error analysis failed: {str(e)}",
            "command": " ".join(cmd) if 'cmd' in locals() else "N/A"
        }


# -----------------
# UTILITY FUNCTIONS
# -----------------

async def run_command_with_env(cmd: List[str], env: Dict[str, str]) -> tuple:
    """
    Run a command asynchronously with custom environment variables.
    
    Args:
        cmd: Command to run as a list of strings
        env: Environment variables dictionary
        
    Returns:
        Tuple of (stdout, stderr) as strings
    """
    print(f"Running command with MCP env: {' '.join(cmd)}")
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env
    )
    
    stdout, stderr = await process.communicate()
    
    stdout_str = stdout.decode('utf-8')
    stderr_str = stderr.decode('utf-8')
    
    if process.returncode != 0:
        error_message = stderr_str if stderr_str else "Unknown error"
        raise Exception(f"Command failed with exit code {process.returncode}: {error_message}")
    
    return stdout_str, stderr_str


async def run_command(cmd: List[str]) -> tuple:
    """Run a command asynchronously and return its stdout and stderr."""
    env = os.environ.copy()
    return await run_command_with_env(cmd, env)


# -----------------
# FILE MANAGEMENT TOOLS
# -----------------

@mcp.tool("list_data_files")
async def list_data_files(directory: Optional[str] = None) -> Dict[str, Any]:
    """
    List all files in a directory, with the default being the data directory.
    
    Args:
        directory: Path to the directory to list (default: ./data)
    """
    try:
        # Default to data directory if none specified
        if directory is None:
            directory = os.path.join(os.getcwd(), "data")
        
        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            return {
                "success": True,
                "directory": directory,
                "files": [],
                "message": f"Directory {directory} was created as it did not exist."
            }
        
        # Check if it's a valid directory
        if not os.path.isdir(directory):
            return {
                "success": False,
                "error": f"{directory} is not a directory."
            }
        
        # Get all files and subdirectories
        all_items = os.listdir(directory)
        
        # Separate files and directories
        files = []
        subdirs = []
        
        for item in all_items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                subdirs.append({
                    "name": item,
                    "type": "directory",
                    "path": item_path
                })
            else:
                # Get file size and modification time
                stat_info = os.stat(item_path)
                size_bytes = stat_info.st_size
                mod_time = stat_info.st_mtime
                
                # Format size for human readability
                if size_bytes < 1024:
                    size_str = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    size_str = f"{size_bytes / 1024:.1f} KB"
                else:
                    size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                
                # Format modification time
                from datetime import datetime
                mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                
                files.append({
                    "name": item,
                    "type": "file",
                    "path": item_path,
                    "size_bytes": size_bytes,
                    "size": size_str,
                    "last_modified": mod_time_str
                })
        
        # Sort both lists by name
        files.sort(key=lambda x: x["name"])
        subdirs.sort(key=lambda x: x["name"])
        
        return {
            "success": True,
            "directory": directory,
            "directories": subdirs,
            "files": files,
            "total_files": len(files),
            "total_directories": len(subdirs)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error listing directory: {str(e)}",
            "directory": directory
        }


# Start the server when the script is run directly
if __name__ == "__main__":
    # Print some debug info
    print(f"Python executable: {PYTHON_EXECUTABLE}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"RTGS CLI path: {RTGS_CLI_PATH}")
    print(f"Device config updater path: {DEVICE_CONFIG_UPDATER_PATH}")
    print(f"Current working directory: {os.getcwd()}")
    
    mcp.run(transport='stdio')