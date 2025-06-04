"""FastMCP server for RTGS Lab Tools - Fixed environment variable handling."""

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

# Get the root directory of the project - this should be where your .env file is
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
print(f"Project root: {PROJECT_ROOT}")

# Load environment variables from .env file if it exists
def load_env_file():
    """Load environment variables from .env file."""
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print(f"Loaded .env file from: {env_file}")
        return True
    else:
        print(f"No .env file found at: {env_file}")
        return False

# Load environment on startup
env_loaded = load_env_file()

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
        # Ensure we're in the correct directory
        original_cwd = os.getcwd()
        os.chdir(PROJECT_ROOT)
        
        # Set MCP environment variables for proper git logging
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        # Build command to call the main CLI
        cmd = [
            PYTHON_EXECUTABLE, "-m", "rtgs_lab_tools.cli", "data",
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
        stdout, stderr = await run_command_with_env(cmd, env, cwd=PROJECT_ROOT)
        
        # Restore original working directory
        os.chdir(original_cwd)
        
        return {
            "success": True,
            "output": stdout,
            "stderr": stderr if stderr else None,
            "command": " ".join(cmd),
            "mcp_execution": True,
            "git_logging_enabled": True,
            "working_directory": str(PROJECT_ROOT)
        }
        
    except Exception as e:
        # Restore original working directory
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
            
        return {
            "success": False,
            "error": f"Data extraction failed: {str(e)}",
            "command": " ".join(cmd) if 'cmd' in locals() else "N/A",
            "mcp_execution": True,
            "env_loaded": env_loaded,
            "project_root": str(PROJECT_ROOT)
        }


@mcp.tool("list_available_projects")
async def list_available_projects() -> Dict[str, Any]:
    """List all available projects in the GEMS Sensing database."""
    try:
        # Ensure we're in the correct directory
        original_cwd = os.getcwd()
        os.chdir(PROJECT_ROOT)
        
        # Set MCP environment variables
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, "-m", "rtgs_lab_tools.cli", "data", "--list-projects"]
        
        stdout, stderr = await run_command_with_env(cmd, env, cwd=PROJECT_ROOT)
        
        # Restore original working directory
        os.chdir(original_cwd)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd)
        }
        
    except Exception as e:
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
            
        return {
            "success": False,
            "error": f"Failed to list projects: {str(e)}",
            "env_loaded": env_loaded
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
        # Ensure we're in the correct directory
        original_cwd = os.getcwd()
        os.chdir(PROJECT_ROOT)
        
        # Set MCP environment variables
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, "-m", "rtgs_lab_tools.cli", "visualize", "--file", file_path, "--format", format]
        
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
        
        stdout, stderr = await run_command_with_env(cmd, env, cwd=PROJECT_ROOT)
        
        # Restore original working directory
        os.chdir(original_cwd)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd),
            "mcp_execution": True,
            "git_logging_enabled": True
        }
        
    except Exception as e:
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
            
        return {
            "success": False,
            "error": f"Visualization failed: {str(e)}",
            "command": " ".join(cmd) if 'cmd' in locals() else "N/A"
        }


@mcp.tool("list_available_parameters")
async def list_available_parameters(file_path: str) -> Dict[str, Any]:
    """List available parameters in a sensor data file."""
    try:
        original_cwd = os.getcwd()
        os.chdir(PROJECT_ROOT)
        
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, "-m", "rtgs_lab_tools.cli", "visualize", "--file", file_path, "--list-params"]
        
        stdout, stderr = await run_command_with_env(cmd, env, cwd=PROJECT_ROOT)
        
        os.chdir(original_cwd)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd)
        }
        
    except Exception as e:
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
            
        return {
            "success": False,
            "error": f"Failed to list parameters: {str(e)}"
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
        original_cwd = os.getcwd()
        os.chdir(PROJECT_ROOT)
        
        # Set MCP environment variables
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, "-m", "rtgs_lab_tools.cli", "analyze-errors", "--file", file_path, "--error-column", error_column]
        
        if generate_graph:
            cmd.append("--generate-graph")
        
        if node_filter:
            cmd.extend(["--nodes", node_filter])
        
        if output_analysis:
            cmd.extend(["--output-analysis", output_analysis])
        
        if note:
            cmd.extend(["--note", note])
        
        stdout, stderr = await run_command_with_env(cmd, env, cwd=PROJECT_ROOT)
        
        os.chdir(original_cwd)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd),
            "mcp_execution": True,
            "git_logging_enabled": True
        }
        
    except Exception as e:
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
            
        return {
            "success": False,
            "error": f"Error analysis failed: {str(e)}",
            "command": " ".join(cmd) if 'cmd' in locals() else "N/A"
        }


@mcp.tool("decode_error_code")
async def decode_error_code(error_code: str) -> Dict[str, Any]:
    """
    Decode a single GEMS device error code.
    
    Args:
        error_code: Hex error code to decode (e.g., "1E01" or "0x1E01")
    """
    try:
        original_cwd = os.getcwd()
        os.chdir(PROJECT_ROOT)
        
        env = os.environ.copy()
        env['MCP_SESSION'] = 'true'
        env['MCP_USER'] = 'claude'
        
        cmd = [PYTHON_EXECUTABLE, "-m", "rtgs_lab_tools.cli", "analyze-errors", "decode", error_code]
        
        stdout, stderr = await run_command_with_env(cmd, env, cwd=PROJECT_ROOT)
        
        os.chdir(original_cwd)
        
        return {
            "success": True,
            "output": stdout,
            "command": " ".join(cmd)
        }
        
    except Exception as e:
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
            
        return {
            "success": False,
            "error": f"Error code decoding failed: {str(e)}"
        }


# -----------------
# UTILITY FUNCTIONS
# -----------------

async def run_command_with_env(cmd: List[str], env: Dict[str, str], cwd: Optional[str] = None) -> tuple:
    """
    Run a command asynchronously with custom environment variables.
    
    Args:
        cmd: Command to run as a list of strings
        env: Environment variables dictionary
        cwd: Working directory for the command
        
    Returns:
        Tuple of (stdout, stderr) as strings
    """
    print(f"Running command with MCP env in {cwd}: {' '.join(cmd)}")
    print(f"DB_USER in env: {'DB_USER' in env}")
    print(f"MCP_SESSION in env: {env.get('MCP_SESSION', 'not set')}")
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
        cwd=cwd
    )
    
    stdout, stderr = await process.communicate()
    
    stdout_str = stdout.decode('utf-8')
    stderr_str = stderr.decode('utf-8')
    
    if process.returncode != 0:
        error_message = stderr_str if stderr_str else "Unknown error"
        raise Exception(f"Command failed with exit code {process.returncode}: {error_message}")
    
    return stdout_str, stderr_str


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
        # Default to data directory in project root if none specified
        if directory is None:
            directory = str(PROJECT_ROOT / "data")
        
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


@mcp.tool("check_environment")
async def check_environment() -> Dict[str, Any]:
    """Check the current environment and configuration status."""
    try:
        env_file = PROJECT_ROOT / ".env"
        
        result = {
            "success": True,
            "project_root": str(PROJECT_ROOT),
            "env_file_exists": env_file.exists(),
            "env_file_path": str(env_file),
            "current_working_directory": os.getcwd(),
            "python_executable": PYTHON_EXECUTABLE,
            "environment_variables": {}
        }
        
        # Check for key environment variables
        key_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'PARTICLE_ACCESS_TOKEN', 'CDS_API_KEY']
        for var in key_vars:
            result["environment_variables"][var] = {
                "exists": var in os.environ,
                "value": "***" if var in os.environ and var in ['DB_PASSWORD', 'PARTICLE_ACCESS_TOKEN', 'CDS_API_KEY'] else os.environ.get(var, "NOT SET")
            }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Environment check failed: {str(e)}"
        }


# Start the server when the script is run directly
if __name__ == "__main__":
    # Print some debug info
    print(f"Python executable: {PYTHON_EXECUTABLE}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Environment loaded: {env_loaded}")
    
    # Check if .env file exists
    env_file = PROJECT_ROOT / ".env"
    print(f".env file exists: {env_file.exists()}")
    if env_file.exists():
        print(f".env file path: {env_file}")
    
    mcp.run(transport='stdio')