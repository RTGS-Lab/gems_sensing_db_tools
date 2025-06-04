"""Error code parsing and analysis for GEMS devices."""

import json
import logging
import re
from collections import Counter
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

import pandas as pd

from ..core.exceptions import ValidationError

logger = logging.getLogger(__name__)

# Error code mappings
ERROR_CLASSES = {
    "0": "Unknown",
    "1": "I2C",
    "2": "Power", 
    "3": "IO",
    "4": "Memory",
    "5": "Timing",
    "6": "Coms",
    "7": "Disagree",
    "8": "Internal",
    "9": "Math/Logical",
    "A": "Sensor",
    "E": "System",
    "F": "Warning"
}

HARDWARE_DEVICES = {
    "0": "System Wide",
    "1": "Port 1 Talon", 
    "2": "Port 2 Talon",
    "3": "Port 3 Talon",
    "4": "Port 4 Talon",
    "E": "Gonk",
    "F": "Kestrel"
}

HARDWARE_SUB_DEVICES = {
    "0": "General",
    "1": "Power",
    "2": "I2C",
    "3": "UART",
    "4": "SPI", 
    "5": "GPIO",
    "6": "ADC",
    "7": "DAC",
    "8": "PWM",
    "9": "Timer"
}


class ErrorCodeParser:
    """Parser for GEMS device error codes."""
    
    def __init__(self):
        """Initialize error code parser."""
        self.error_classes = ERROR_CLASSES
        self.hardware_devices = HARDWARE_DEVICES
        self.hardware_sub_devices = HARDWARE_SUB_DEVICES
    
    def parse_error_code(self, error_code: Union[str, int]) -> Dict[str, str]:
        """Parse a single error code into components.
        
        Args:
            error_code: Error code as string or integer
            
        Returns:
            Dictionary with parsed error components
            
        Raises:
            ValidationError: If error code format is invalid
        """
        try:
            # Convert to string and normalize
            code_str = str(error_code).upper().strip()
            
            # Remove 0x prefix if present
            if code_str.startswith('0X'):
                code_str = code_str[2:]
            
            # Validate length (should be 4 hex digits)
            if len(code_str) != 4:
                raise ValidationError(f"Error code must be 4 hex digits, got: {code_str}")
            
            # Parse components
            error_class = code_str[0]
            hardware_device = code_str[1] 
            hardware_sub_device = code_str[2]
            specific_error = code_str[3]
            
            # Look up descriptions
            parsed = {
                'raw_code': error_code,
                'normalized_code': code_str,
                'error_class': error_class,
                'error_class_name': self.error_classes.get(error_class, f"Unknown Class ({error_class})"),
                'hardware_device': hardware_device,
                'hardware_device_name': self.hardware_devices.get(hardware_device, f"Unknown Device ({hardware_device})"),
                'hardware_sub_device': hardware_sub_device,
                'hardware_sub_device_name': self.hardware_sub_devices.get(hardware_sub_device, f"Unknown Sub-device ({hardware_sub_device})"),
                'specific_error': specific_error,
                'full_description': self._generate_description(error_class, hardware_device, hardware_sub_device, specific_error)
            }
            
            return parsed
            
        except Exception as e:
            raise ValidationError(f"Failed to parse error code '{error_code}': {e}")
    
    def _generate_description(self, error_class: str, device: str, sub_device: str, specific: str) -> str:
        """Generate human-readable error description."""
        class_name = self.error_classes.get(error_class, f"Unknown ({error_class})")
        device_name = self.hardware_devices.get(device, f"Unknown Device ({device})")
        sub_device_name = self.hardware_sub_devices.get(sub_device, f"Unknown Sub-device ({sub_device})")
        
        return f"{class_name} error on {device_name} - {sub_device_name} (Code: {specific})"
    
    def parse_error_codes_from_data(self, df: pd.DataFrame, error_column: str = 'message') -> pd.DataFrame:
        """Parse error codes from a DataFrame with JSON messages.
        
        Args:
            df: DataFrame containing error data
            error_column: Column name containing JSON error data
            
        Returns:
            DataFrame with parsed error information
        """
        parsed_errors = []
        
        for _, row in df.iterrows():
            try:
                # Parse JSON message
                if error_column in row:
                    message = row[error_column]
                    
                    if isinstance(message, str):
                        try:
                            data = json.loads(message)
                        except json.JSONDecodeError:
                            continue
                    else:
                        data = message
                    
                    # Extract error codes from various possible locations
                    error_codes = self._extract_error_codes_from_json(data)
                    
                    for error_code in error_codes:
                        parsed_error = self.parse_error_code(error_code)
                        
                        # Add metadata from original row
                        error_entry = {
                            'timestamp': row.get('publish_time', row.get('timestamp')),
                            'node_id': row.get('node_id'),
                            'original_message': message,
                            **parsed_error
                        }
                        parsed_errors.append(error_entry)
                        
            except Exception as e:
                logger.warning(f"Failed to parse error from row: {e}")
                continue
        
        if not parsed_errors:
            return pd.DataFrame()
        
        return pd.DataFrame(parsed_errors)
    
    def _extract_error_codes_from_json(self, data: Dict[str, Any]) -> List[str]:
        """Extract error codes from JSON data structure."""
        error_codes = []
        
        # Common error code locations in GEMS data
        possible_paths = [
            ['Error', 'Code'],
            ['Diagnostic', 'Error'],
            ['Status', 'Error'],
            ['error_code'],
            ['error'],
            ['errors']
        ]
        
        for path in possible_paths:
            value = data
            for key in path:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    value = None
                    break
            
            if value is not None:
                if isinstance(value, list):
                    error_codes.extend([str(v) for v in value])
                else:
                    error_codes.append(str(value))
        
        # Also look for hex patterns in string values
        error_codes.extend(self._find_hex_patterns(str(data)))
        
        return list(set(error_codes))  # Remove duplicates
    
    def _find_hex_patterns(self, text: str) -> List[str]:
        """Find 4-digit hex patterns that could be error codes."""
        # Pattern for 4-digit hex codes, optionally prefixed with 0x
        pattern = r'\b(?:0[xX])?([0-9A-Fa-f]{4})\b'
        matches = re.findall(pattern, text)
        return matches


def parse_error_codes(
    df: pd.DataFrame, 
    error_column: str = 'message'
) -> pd.DataFrame:
    """Convenience function to parse error codes from data.
    
    Args:
        df: DataFrame with error data
        error_column: Column containing error information
        
    Returns:
        DataFrame with parsed errors
    """
    parser = ErrorCodeParser()
    return parser.parse_error_codes_from_data(df, error_column)


def analyze_error_patterns(
    parsed_errors_df: pd.DataFrame,
    group_by: str = 'error_class_name',
    time_window: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze error patterns and generate statistics.
    
    Args:
        parsed_errors_df: DataFrame with parsed error data
        group_by: Column to group errors by
        time_window: Optional time window for grouping ('D', 'H', etc.)
        
    Returns:
        Dictionary with error analysis results
    """
    if parsed_errors_df.empty:
        return {'total_errors': 0, 'patterns': {}}
    
    analysis = {
        'total_errors': len(parsed_errors_df),
        'unique_error_codes': parsed_errors_df['normalized_code'].nunique(),
        'date_range': {
            'start': parsed_errors_df['timestamp'].min(),
            'end': parsed_errors_df['timestamp'].max()
        }
    }
    
    # Error frequency by category
    if group_by in parsed_errors_df.columns:
        error_counts = parsed_errors_df[group_by].value_counts()
        analysis['error_frequency'] = error_counts.to_dict()
    
    # Top error codes
    top_codes = parsed_errors_df.groupby(['normalized_code', 'full_description']).size().sort_values(ascending=False).head(10)
    analysis['top_error_codes'] = [
        {'code': code, 'description': desc, 'count': count}
        for (code, desc), count in top_codes.items()
    ]
    
    # Errors by device
    if 'hardware_device_name' in parsed_errors_df.columns:
        device_errors = parsed_errors_df['hardware_device_name'].value_counts()
        analysis['errors_by_device'] = device_errors.to_dict()
    
    # Errors by node
    if 'node_id' in parsed_errors_df.columns:
        node_errors = parsed_errors_df['node_id'].value_counts()
        analysis['errors_by_node'] = node_errors.to_dict()
    
    # Temporal patterns
    if time_window and 'timestamp' in parsed_errors_df.columns:
        df_copy = parsed_errors_df.copy()
        df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'])
        temporal_counts = df_copy.set_index('timestamp').resample(time_window).size()
        analysis['temporal_pattern'] = temporal_counts.to_dict()
    
    logger.info(f"Analyzed {analysis['total_errors']} errors with {analysis['unique_error_codes']} unique codes")
    
    return analysis