"""RTGS Lab Tools - Environmental sensing and climate data toolkit."""

__version__ = "0.1.0"
__author__ = "RTGS Lab"
__email__ = "rtgs@umn.edu"

# Core infrastructure
from .core import DatabaseManager, Config
from .core.git_logger import GitLogger
from .core.exceptions import ValidationError, DatabaseError, APIError

# High-level data extraction functions
from .sensing_data import extract_data, list_available_projects, get_raw_data

# Visualization functions
from .visualization import create_time_series_plot, create_multi_parameter_plot, parse_sensor_messages

# Device management
from .device_configuration import ParticleConfigUpdater, ParticleClient

# Error analysis
from .error_analysis import ErrorCodeParser

# Climate data
from .gridded_data import ERA5Client, download_era5_data, process_era5_data

__all__ = [
    # Core
    "DatabaseManager",
    "Config", 
    "GitLogger",
    "ValidationError",
    "DatabaseError", 
    "APIError",
    
    # Data extraction
    "extract_data",
    "list_available_projects",
    "get_raw_data",
    
    # Visualization
    "create_time_series_plot",
    "create_multi_parameter_plot", 
    "parse_sensor_messages",
    
    # Device management
    "ParticleConfigUpdater",
    "ParticleClient",
    "ErrorCodeParser",
    
    # Climate data
    "ERA5Client",
    "download_era5_data",
    "process_era5_data",
]