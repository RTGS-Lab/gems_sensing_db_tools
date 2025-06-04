#!/usr/bin/env python3
"""
Particle Device Configuration Updater with Git Logging

This script updates configurations on multiple Particle devices, verifies the updates,
and automatically commits execution logs to the repository for audit purposes.

This version maintains full compatibility with the original update_device_configurations.py
while using the shared GitLogger from core.
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests
import threading

from ..core import GitLogger
from ..core.exceptions import APIError, ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('particle_config_update.log')
    ]
)
logger = logging.getLogger(__name__)


class ParticleConfigUpdater:
    """Particle device configuration updater with git logging."""
    
    def __init__(self, enable_git_logging: bool = True, repo_path: Optional[str] = None):
        """Initialize the configuration updater.
        
        Args:
            enable_git_logging: Whether to enable git logging
            repo_path: Path to git repository (optional)
        """
        self.access_token = os.environ.get('PARTICLE_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("PARTICLE_ACCESS_TOKEN env variable is required")
        
        self.base_url = "https://api.particle.io/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        # Configuration for retries and timeouts
        self.max_retries = 3
        self.restart_wait_time = 30  # seconds to wait for device restart
        self.online_check_timeout = 120  # seconds to wait for device to come online
        self.uid_check_retries = 5
        self.max_concurrent_devices = 5  # Maximum devices to process simultaneously
        
        # Thread-safe counters
        self._lock = threading.Lock()
        self._processed_count = 0
        
        # Git logging
        self.enable_git_logging = enable_git_logging
        if enable_git_logging:
            self.git_logger = GitLogger(tool_name="device-configuration", repo_path=repo_path)
        
    def load_config_from_file(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config_data
        except FileNotFoundError:
            raise ValidationError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in configuration file: {e}")
    
    def load_config_from_string(self, config_str: str) -> Dict[str, Any]:
        """Load configuration from JSON string."""
        try:
            config_data = json.loads(config_str)
            logger.info("Loaded configuration from string")
            return config_data
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in configuration string: {e}")
    
    def load_devices_from_file(self, devices_path: str) -> List[str]:
        """Load device list from file."""
        try:
            with open(devices_path, 'r') as f:
                device_ids = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            logger.info(f"Loaded {len(device_ids)} devices from {devices_path}")
            return device_ids
        except FileNotFoundError:
            raise ValidationError(f"Device list file not found: {devices_path}")
    
    def load_devices_from_string(self, devices_str: str) -> List[str]:
        """Load device list from comma-separated string."""
        device_ids = [device.strip() for device in devices_str.split(',') if device.strip()]
        logger.info(f"Loaded {len(device_ids)} devices from string")
        return device_ids
    
    def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """Validate configuration structure."""
        required_keys = ['config']
        for key in required_keys:
            if key not in config:
                raise ValidationError(f"Missing required key in configuration: {key}")
        
        if 'system' not in config['config']:
            raise ValidationError("Missing 'system' configuration")
        
        # Validate system configuration
        system_config = config['config']['system']
        required_system_keys = ['logPeriod', 'backhaulCount', 'powerSaveMode', 'loggingMode']
        for key in required_system_keys:
            if key not in system_config:
                logger.warning(f"Missing recommended system configuration key: {key}")
        
        return True
    
    def call_device_function(self, device_id: str, function_name: str, argument: str = "") -> Dict[str, Any]:
        """Call a function on a Particle device."""
        url = f"{self.base_url}/devices/{device_id}/{function_name}"
        data = {'arg': argument}
        
        try:
            response = self.session.post(url, data=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to call function {function_name} on device {device_id}: {e}")
    
    def get_device_variable(self, device_id: str, variable_name: str) -> Any:
        """Get a variable value from a Particle device."""
        url = f"{self.base_url}/devices/{device_id}/{variable_name}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get('result')
        except requests.RequestException as e:
            raise APIError(f"Failed to get variable {variable_name} from device {device_id}: {e}")
    
    def encode_configuration_uids(self, config: Dict[str, Any]) -> Tuple[int, int]:
        """Encode configuration into system and sensor UIDs."""
        system_config = config['config']['system']
        sensor_config = config['config'].get('sensors', {})
        
        # Encode system UID (simplified version)
        system_uid = (
            (system_config.get('logPeriod', 300) & 0xFFFF) |
            ((system_config.get('backhaulCount', 4) & 0xFF) << 16) |
            ((system_config.get('powerSaveMode', 1) & 0xFF) << 24)
        )
        
        # Encode sensor UID (simplified version)
        sensor_uid = (
            (sensor_config.get('numSoil', 0) & 0xFF) |
            ((sensor_config.get('numET', 0) & 0xFF) << 8) |
            ((sensor_config.get('numCO2', 0) & 0xFF) << 16) |
            ((sensor_config.get('numPressure', 0) & 0xFF) << 24)
        )
        
        return system_uid, sensor_uid
    
    def update_single_device(self, device_id: str, config: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
        """Update configuration on a single device."""
        start_time = time.time()
        device_result = {
            'device_id': device_id,
            'success': False,
            'start_time': datetime.now().isoformat()
        }
        
        try:
            if args.dry_run:
                logger.info(f"DRY RUN: Would update device {device_id}")
                device_result.update({
                    'success': True,
                    'dry_run': True,
                    'duration': time.time() - start_time,
                    'end_time': datetime.now().isoformat()
                })
                return device_result
            
            # Encode configuration UIDs
            system_uid, sensor_uid = self.encode_configuration_uids(config)
            
            logger.info(f"Updating device {device_id} with system UID: {system_uid}, sensor UID: {sensor_uid}")
            
            # Update system configuration
            system_result = self.call_device_function(
                device_id, 
                "updateSystemConfig", 
                str(system_uid)
            )
            
            # Update sensor configuration
            sensor_result = self.call_device_function(
                device_id,
                "updateSensorConfig", 
                str(sensor_uid)
            )
            
            # Wait for device restart
            logger.info(f"Waiting {args.restart_wait}s for device {device_id} to restart...")
            time.sleep(args.restart_wait)
            
            # Verify configuration if not in dry run
            verification_success = True
            if not args.dry_run:
                verification_success = self.verify_device_configuration(
                    device_id, system_uid, sensor_uid, args.online_timeout
                )
            
            device_result.update({
                'success': verification_success,
                'system_uid': system_uid,
                'sensor_uid': sensor_uid,
                'system_function_result': system_result,
                'sensor_function_result': sensor_result,
                'verification_passed': verification_success,
                'duration': time.time() - start_time,
                'end_time': datetime.now().isoformat()
            })
            
            with self._lock:
                self._processed_count += 1
                logger.info(f"Device {device_id}: {'SUCCESS' if verification_success else 'FAILED'} "
                           f"({self._processed_count} processed)")
            
        except Exception as e:
            device_result.update({
                'success': False,
                'error': str(e),
                'duration': time.time() - start_time,
                'end_time': datetime.now().isoformat()
            })
            logger.error(f"Failed to update device {device_id}: {e}")
        
        return device_result
    
    def verify_device_configuration(self, device_id: str, expected_system_uid: int, 
                                  expected_sensor_uid: int, timeout: int) -> bool:
        """Verify that device configuration was applied correctly."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check if device is online and responsive
                system_uid = self.get_device_variable(device_id, "systemUID")
                sensor_uid = self.get_device_variable(device_id, "sensorUID")
                
                if system_uid == expected_system_uid and sensor_uid == expected_sensor_uid:
                    logger.info(f"Device {device_id} configuration verified successfully")
                    return True
                
                logger.debug(f"Device {device_id} UIDs not yet updated: "
                           f"system={system_uid}/{expected_system_uid}, "
                           f"sensor={sensor_uid}/{expected_sensor_uid}")
                
            except Exception as e:
                logger.debug(f"Verification attempt failed for {device_id}: {e}")
            
            time.sleep(5)  # Wait before next check
        
        logger.error(f"Device {device_id} configuration verification failed after {timeout}s")
        return False
    
    def update_multiple_devices(self, device_ids: List[str], config: Dict[str, Any], 
                              args: argparse.Namespace) -> Dict[str, Any]:
        """Update configuration on multiple devices concurrently."""
        start_time = datetime.now()
        
        logger.info(f"Starting configuration update for {len(device_ids)} devices")
        logger.info(f"Max concurrent: {args.max_concurrent}, Max retries: {args.max_retries}")
        
        # Reset counter
        with self._lock:
            self._processed_count = 0
        
        device_results = []
        
        # Process devices concurrently
        with ThreadPoolExecutor(max_workers=args.max_concurrent) as executor:
            future_to_device = {
                executor.submit(self.update_single_device, device_id, config, args): device_id
                for device_id in device_ids
            }
            
            for future in as_completed(future_to_device):
                device_id = future_to_device[future]
                try:
                    result = future.result()
                    device_results.append(result)
                except Exception as e:
                    logger.error(f"Unexpected error processing device {device_id}: {e}")
                    device_results.append({
                        'device_id': device_id,
                        'success': False,
                        'error': f"Unexpected error: {e}",
                        'end_time': datetime.now().isoformat()
                    })
        
        end_time = datetime.now()
        
        # Calculate summary
        successful = sum(1 for r in device_results if r['success'])
        failed = len(device_results) - successful
        
        # Encode expected UIDs for summary
        expected_system_uid, expected_sensor_uid = self.encode_configuration_uids(config)
        
        summary = {
            'total_devices': len(device_ids),
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / len(device_ids) * 100) if device_ids else 0,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration': (end_time - start_time).total_seconds(),
            'expected_system_uid': expected_system_uid,
            'expected_sensor_uid': expected_sensor_uid
        }
        
        results = {
            'summary': summary,
            'device_results': device_results,
            'configuration': config,
            'parameters': vars(args)
        }
        
        logger.info(f"Configuration update completed: {successful}/{len(device_ids)} successful")
        
        # Create git log if enabled
        if self.enable_git_logging:
            try:
                self.git_logger.log_execution(
                    operation=f"Update {len(device_ids)} device configurations",
                    parameters=vars(args),
                    results=results,
                    script_path=__file__,
                    additional_sections={
                        "Configuration Applied": f"```json\n{json.dumps(config, indent=2)}\n```",
                        "Device Results": self._format_device_results(device_results)
                    }
                )
            except Exception as e:
                logger.error(f"Failed to create git log: {e}")
        
        return results
    
    def _format_device_results(self, device_results: List[Dict[str, Any]]) -> str:
        """Format device results for markdown display."""
        lines = []
        for result in device_results:
            status = "✅" if result['success'] else "❌"
            device_id = result['device_id']
            
            if result['success']:
                system_uid = result.get('system_uid', 'N/A')
                sensor_uid = result.get('sensor_uid', 'N/A')
                lines.append(f"- {status} `{device_id}` - Success (System UID: {system_uid}, Sensor UID: {sensor_uid})")
            else:
                error = result.get('error', 'Unknown error')
                lines.append(f"- {status} `{device_id}` - Failed: {error}")
        
        return "\n".join(lines)


def main():
    """Main function matching original script interface."""
    parser = argparse.ArgumentParser(description="Update configurations on multiple Particle devices")
    parser.add_argument("--config", required=True, 
                       help="Configuration as JSON string or path to JSON file")
    parser.add_argument("--devices", required=True,
                       help="Device IDs as comma-separated string or path to device list file")
    parser.add_argument("--output", default="update_results.json",
                       help="Output file for detailed results")
    parser.add_argument("--max-retries", type=int, default=3,
                       help="Maximum retry attempts per device")
    parser.add_argument("--restart-wait", type=int, default=30,
                       help="Seconds to wait for device restart")
    parser.add_argument("--online-timeout", type=int, default=120,
                       help="Seconds to wait for device to come online")
    parser.add_argument("--max-concurrent", type=int, default=5,
                       help="Maximum concurrent devices to process")
    parser.add_argument("--dry-run", action="store_true",
                       help="Validate inputs without making changes")
    parser.add_argument("--note", default="configuration update",
                       help="Note describing the purpose of this update")
    parser.add_argument("--no-git-log", action="store_true",
                       help="Disable git logging")
    
    args = parser.parse_args()
    
    try:
        # Initialize updater
        updater = ParticleConfigUpdater(enable_git_logging=not args.no_git_log)
        
        # Load configuration
        if os.path.isfile(args.config):
            config = updater.load_config_from_file(args.config)
        else:
            config = updater.load_config_from_string(args.config)
        
        # Validate configuration
        updater.validate_configuration(config)
        
        # Load device list
        if os.path.isfile(args.devices):
            device_ids = updater.load_devices_from_file(args.devices)
        else:
            device_ids = updater.load_devices_from_string(args.devices)
        
        if not device_ids:
            raise ValidationError("No devices specified")
        
        logger.info(f"Starting update for {len(device_ids)} devices")
        if args.dry_run:
            logger.info("DRY RUN MODE - No actual changes will be made")
        
        # Update devices
        results = updater.update_multiple_devices(device_ids, config, args)
        
        # Save results to file
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {args.output}")
        
        # Exit with appropriate code
        if results['summary']['failed'] > 0:
            logger.error(f"Some devices failed to update: {results['summary']['failed']}/{results['summary']['total_devices']}")
            sys.exit(1)
        else:
            logger.info("All devices updated successfully")
            sys.exit(0)
        
    except Exception as e:
        logger.error(f"Configuration update failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()