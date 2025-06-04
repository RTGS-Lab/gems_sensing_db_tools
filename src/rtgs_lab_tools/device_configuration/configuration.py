"""Configuration management and UID decoding for GEMS devices."""

import json
import logging
import time
from typing import Dict, Any, List, Optional, Union

from ..core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def decode_system_uid(uid: Union[int, str]) -> Dict[str, Any]:
    """Decode the system configuration UID.
    
    Args:
        uid: The encoded system configuration UID (int or hex string)
        
    Returns:
        Dictionary containing decoded configuration values
        
    Raises:
        ValidationError: If UID format is invalid
    """
    try:
        # Convert hex string to int if needed
        if isinstance(uid, str):
            if uid.startswith('0x') or uid.startswith('0X'):
                uid = int(uid, 16)
            else:
                uid = int(uid)
        
        config = {}
        
        # Extract each field using bit masks and shifts
        # Based on the original configuration_uid_decoder.py
        config['sampling_interval'] = (uid >> 0) & 0xFFFF  # 16 bits
        config['upload_interval'] = (uid >> 16) & 0xFFFF   # 16 bits
        config['gps_acquisition_timeout'] = (uid >> 32) & 0xFFFF  # 16 bits
        config['gps_acquisition_interval'] = (uid >> 48) & 0xFFFF  # 16 bits
        
        logger.info(f"Decoded system UID {hex(uid)}: {config}")
        return config
        
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Invalid system UID format: {e}")


def decode_sensor_uid(uid: Union[int, str]) -> Dict[str, Any]:
    """Decode the sensor configuration UID.
    
    Args:
        uid: The encoded sensor configuration UID (int or hex string)
        
    Returns:
        Dictionary containing decoded sensor configuration
        
    Raises:
        ValidationError: If UID format is invalid
    """
    try:
        # Convert hex string to int if needed
        if isinstance(uid, str):
            if uid.startswith('0x') or uid.startswith('0X'):
                uid = int(uid, 16)
            else:
                uid = int(uid)
        
        config = {}
        
        # Extract sensor configuration fields
        # Based on the original configuration_uid_decoder.py
        config['sensor_count'] = (uid >> 0) & 0xFF  # 8 bits
        config['sensor_types'] = []
        
        # Extract individual sensor configurations (simplified)
        for i in range(min(config['sensor_count'], 8)):  # Max 8 sensors
            sensor_bits = (uid >> (8 + i * 8)) & 0xFF
            config['sensor_types'].append({
                'type': sensor_bits & 0x0F,
                'enabled': bool(sensor_bits & 0x10),
                'config': (sensor_bits >> 5) & 0x07
            })
        
        logger.info(f"Decoded sensor UID {hex(uid)}: {config}")
        return config
        
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Invalid sensor UID format: {e}")


class ConfigurationManager:
    """Manages device configurations for GEMS sensing devices."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration JSON file
        """
        self.config_file = config_file
        self.configurations = {}
        
        if config_file:
            self.load_configurations(config_file)
    
    def load_configurations(self, config_file: str):
        """Load configurations from JSON file.
        
        Args:
            config_file: Path to configuration file
            
        Raises:
            ValidationError: If file cannot be loaded or parsed
        """
        try:
            with open(config_file, 'r') as f:
                self.configurations = json.load(f)
            
            logger.info(f"Loaded {len(self.configurations)} configurations from {config_file}")
            
        except FileNotFoundError:
            raise ValidationError(f"Configuration file not found: {config_file}")
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in configuration file: {e}")
    
    def get_configuration(self, name: str) -> Dict[str, Any]:
        """Get a configuration by name.
        
        Args:
            name: Configuration name
            
        Returns:
            Configuration dictionary
            
        Raises:
            ValidationError: If configuration not found
        """
        if name not in self.configurations:
            raise ValidationError(f"Configuration '{name}' not found")
        
        return self.configurations[name]
    
    def list_configurations(self) -> List[str]:
        """List available configuration names.
        
        Returns:
            List of configuration names
        """
        return list(self.configurations.keys())
    
    def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """Validate a configuration structure.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If configuration is invalid
        """
        required_fields = ['sampling_interval', 'upload_interval']
        
        for field in required_fields:
            if field not in config:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate value ranges
        if config['sampling_interval'] <= 0:
            raise ValidationError("Sampling interval must be positive")
        
        if config['upload_interval'] <= 0:
            raise ValidationError("Upload interval must be positive")
        
        logger.info("Configuration validation passed")
        return True
    
    def encode_system_uid(self, config: Dict[str, Any]) -> int:
        """Encode system configuration into UID.
        
        Args:
            config: System configuration dictionary
            
        Returns:
            Encoded UID as integer
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.validate_configuration(config)
        
        try:
            uid = 0
            uid |= (config['sampling_interval'] & 0xFFFF) << 0
            uid |= (config['upload_interval'] & 0xFFFF) << 16
            uid |= (config.get('gps_acquisition_timeout', 0) & 0xFFFF) << 32
            uid |= (config.get('gps_acquisition_interval', 0) & 0xFFFF) << 48
            
            logger.info(f"Encoded system configuration to UID: {hex(uid)}")
            return uid
            
        except (KeyError, TypeError) as e:
            raise ValidationError(f"Failed to encode configuration: {e}")
    
    def create_configuration_payload(
        self, 
        system_config: Dict[str, Any],
        sensor_configs: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create configuration payload for device update.
        
        Args:
            system_config: System configuration
            sensor_configs: Optional sensor configurations
            
        Returns:
            Configuration payload for device
        """
        payload = {
            'system_uid': self.encode_system_uid(system_config),
            'system_config': system_config,
            'timestamp': int(time.time())
        }
        
        if sensor_configs:
            payload['sensor_configs'] = sensor_configs
            # Note: Sensor UID encoding would be implemented based on 
            # specific sensor configuration requirements
        
        return payload