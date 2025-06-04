"""Device configuration update management with logging and verification."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .particle_client import ParticleClient
from .configuration import ConfigurationManager
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class DeviceConfigurationUpdater:
    """Manages configuration updates for multiple devices with verification."""
    
    def __init__(
        self, 
        particle_client: Optional[ParticleClient] = None,
        config_manager: Optional[ConfigurationManager] = None
    ):
        """Initialize device updater.
        
        Args:
            particle_client: Particle API client
            config_manager: Configuration manager
        """
        self.particle_client = particle_client or ParticleClient()
        self.config_manager = config_manager or ConfigurationManager()
        self.update_logs = []
    
    def update_device_configuration(
        self,
        device_id: str,
        configuration: Dict[str, Any],
        verify: bool = True,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Update configuration on a single device.
        
        Args:
            device_id: Device ID to update
            configuration: Configuration to apply
            verify: Whether to verify the update
            timeout: Timeout for update verification
            
        Returns:
            Update result dictionary
            
        Raises:
            APIError: If device communication fails
            ValidationError: If configuration is invalid
        """
        start_time = time.time()
        result = {
            'device_id': device_id,
            'status': 'started',
            'start_time': datetime.now().isoformat(),
            'configuration': configuration
        }
        
        try:
            # Validate configuration
            self.config_manager.validate_configuration(configuration)
            
            # Create configuration payload
            payload = self.config_manager.create_configuration_payload(configuration)
            
            # Call update function on device
            logger.info(f"Updating configuration on device {device_id}")
            update_result = self.particle_client.call_function(
                device_id=device_id,
                function_name="updateConfig",
                argument=str(payload['system_uid'])
            )
            
            result['function_result'] = update_result
            result['status'] = 'update_sent'
            
            # Verify update if requested
            if verify:
                logger.info(f"Verifying configuration update on {device_id}")
                verification = self._verify_configuration_update(
                    device_id, 
                    payload['system_uid'],
                    timeout
                )
                result['verification'] = verification
                result['status'] = 'verified' if verification['success'] else 'verification_failed'
            else:
                result['status'] = 'completed'
            
            result['duration'] = time.time() - start_time
            result['end_time'] = datetime.now().isoformat()
            
            logger.info(f"Configuration update for {device_id}: {result['status']}")
            return result
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['duration'] = time.time() - start_time
            result['end_time'] = datetime.now().isoformat()
            
            logger.error(f"Configuration update failed for {device_id}: {e}")
            raise
    
    def update_multiple_devices(
        self,
        device_ids: List[str],
        configuration: Dict[str, Any],
        max_workers: int = 5,
        verify: bool = True
    ) -> Dict[str, Any]:
        """Update configuration on multiple devices concurrently.
        
        Args:
            device_ids: List of device IDs to update
            configuration: Configuration to apply
            max_workers: Maximum number of concurrent updates
            verify: Whether to verify updates
            
        Returns:
            Summary of all updates
        """
        start_time = time.time()
        results = {}
        
        logger.info(f"Starting configuration update for {len(device_ids)} devices")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all update tasks
            future_to_device = {
                executor.submit(
                    self.update_device_configuration,
                    device_id,
                    configuration,
                    verify
                ): device_id
                for device_id in device_ids
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_device):
                device_id = future_to_device[future]
                try:
                    result = future.result()
                    results[device_id] = result
                except Exception as e:
                    results[device_id] = {
                        'device_id': device_id,
                        'status': 'failed',
                        'error': str(e),
                        'end_time': datetime.now().isoformat()
                    }
        
        # Create summary
        summary = {
            'total_devices': len(device_ids),
            'successful': len([r for r in results.values() if r['status'] in ['completed', 'verified']]),
            'failed': len([r for r in results.values() if r['status'] == 'failed']),
            'verification_failed': len([r for r in results.values() if r['status'] == 'verification_failed']),
            'duration': time.time() - start_time,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        logger.info(f"Batch update completed: {summary['successful']}/{summary['total_devices']} successful")
        self.update_logs.append(summary)
        
        return summary
    
    def _verify_configuration_update(
        self,
        device_id: str,
        expected_uid: int,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Verify that configuration was applied correctly.
        
        Args:
            device_id: Device to verify
            expected_uid: Expected configuration UID
            timeout: Verification timeout
            
        Returns:
            Verification result
        """
        verification = {
            'success': False,
            'attempts': 0,
            'max_attempts': timeout // 5  # Check every 5 seconds
        }
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                verification['attempts'] += 1
                
                # Read current configuration UID from device
                current_uid = self.particle_client.get_variable(
                    device_id, 
                    "configUID"
                )
                
                if current_uid == expected_uid:
                    verification['success'] = True
                    verification['current_uid'] = current_uid
                    verification['duration'] = time.time() - start_time
                    break
                
                logger.debug(f"Verification attempt {verification['attempts']}: "
                           f"expected {expected_uid}, got {current_uid}")
                
                time.sleep(5)  # Wait before next attempt
                
            except APIError as e:
                logger.warning(f"Verification attempt {verification['attempts']} failed: {e}")
                time.sleep(5)
        
        if not verification['success']:
            verification['error'] = f"Configuration not verified after {timeout}s"
        
        return verification
    
    def load_device_list(self, file_path: str) -> List[str]:
        """Load device IDs from file.
        
        Args:
            file_path: Path to file with device IDs (one per line)
            
        Returns:
            List of device IDs
            
        Raises:
            ValidationError: If file cannot be read
        """
        try:
            with open(file_path, 'r') as f:
                device_ids = [line.strip() for line in f if line.strip()]
            
            logger.info(f"Loaded {len(device_ids)} device IDs from {file_path}")
            return device_ids
            
        except FileNotFoundError:
            raise ValidationError(f"Device list file not found: {file_path}")
        except Exception as e:
            raise ValidationError(f"Failed to load device list: {e}")
    
    def get_update_summary(self) -> Dict[str, Any]:
        """Get summary of all configuration updates.
        
        Returns:
            Summary of update history
        """
        if not self.update_logs:
            return {'total_updates': 0, 'updates': []}
        
        total_devices = sum(log['total_devices'] for log in self.update_logs)
        total_successful = sum(log['successful'] for log in self.update_logs)
        
        return {
            'total_updates': len(self.update_logs),
            'total_devices_updated': total_devices,
            'total_successful': total_successful,
            'success_rate': total_successful / total_devices if total_devices > 0 else 0,
            'updates': self.update_logs
        }
    
    def save_update_log(self, file_path: str, summary: Dict[str, Any]):
        """Save update log to file.
        
        Args:
            file_path: Path to save log file
            summary: Update summary to save
        """
        try:
            log_path = Path(file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_path, 'w') as f:
                import json
                json.dump(summary, f, indent=2)
            
            logger.info(f"Update log saved to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save update log: {e}")
            raise