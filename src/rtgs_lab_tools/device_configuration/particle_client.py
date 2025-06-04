"""Particle API client for device management."""

import logging
from typing import Any, Dict, List, Optional

import requests

from ..core import Config
from ..core.exceptions import APIError

logger = logging.getLogger(__name__)


class ParticleClient:
    """Client for interacting with Particle Cloud API."""
    
    def __init__(self, access_token: Optional[str] = None):
        """Initialize Particle client.
        
        Args:
            access_token: Particle access token. If None, reads from config.
        """
        self.access_token = access_token or Config().particle_access_token
        if not self.access_token:
            raise APIError("Particle access token not found. Set PARTICLE_ACCESS_TOKEN environment variable.")
        
        self.base_url = "https://api.particle.io/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """List all devices in the account.
        
        Returns:
            List of device information dictionaries
            
        Raises:
            APIError: If API request fails
        """
        try:
            response = self.session.get(f"{self.base_url}/devices")
            response.raise_for_status()
            
            devices = response.json()
            logger.info(f"Retrieved {len(devices)} devices")
            return devices
            
        except requests.RequestException as e:
            logger.error(f"Failed to list devices: {e}")
            raise APIError(f"Failed to list devices: {e}")
    
    def get_device(self, device_id: str) -> Dict[str, Any]:
        """Get information about a specific device.
        
        Args:
            device_id: Device ID or name
            
        Returns:
            Device information dictionary
        """
        try:
            response = self.session.get(f"{self.base_url}/devices/{device_id}")
            response.raise_for_status()
            
            device = response.json()
            logger.info(f"Retrieved device info for {device_id}")
            return device
            
        except requests.RequestException as e:
            logger.error(f"Failed to get device {device_id}: {e}")
            raise APIError(f"Failed to get device: {e}")
    
    def call_function(
        self, 
        device_id: str, 
        function_name: str, 
        argument: str = ""
    ) -> Dict[str, Any]:
        """Call a function on a device.
        
        Args:
            device_id: Device ID or name
            function_name: Name of function to call
            argument: Function argument
            
        Returns:
            Function call result
        """
        try:
            data = {"arg": argument}
            response = self.session.post(
                f"{self.base_url}/devices/{device_id}/{function_name}",
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Called function {function_name} on {device_id}")
            return result
            
        except requests.RequestException as e:
            logger.error(f"Failed to call function {function_name} on {device_id}: {e}")
            raise APIError(f"Failed to call function: {e}")
    
    def get_variable(self, device_id: str, variable_name: str) -> Any:
        """Get a variable value from a device.
        
        Args:
            device_id: Device ID or name  
            variable_name: Name of variable to read
            
        Returns:
            Variable value
        """
        try:
            response = self.session.get(
                f"{self.base_url}/devices/{device_id}/{variable_name}"
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Read variable {variable_name} from {device_id}")
            return result.get("result")
            
        except requests.RequestException as e:
            logger.error(f"Failed to read variable {variable_name} from {device_id}: {e}")
            raise APIError(f"Failed to read variable: {e}")
    
    def ping_device(self, device_id: str) -> bool:
        """Ping a device to check if it's online.
        
        Args:
            device_id: Device ID or name
            
        Returns:
            True if device responds, False otherwise
        """
        try:
            response = self.session.put(f"{self.base_url}/devices/{device_id}/ping")
            response.raise_for_status()
            
            result = response.json()
            online = result.get("online", False)
            logger.info(f"Device {device_id} ping: {'online' if online else 'offline'}")
            return online
            
        except requests.RequestException as e:
            logger.error(f"Failed to ping device {device_id}: {e}")
            raise APIError(f"Failed to ping device: {e}")
    
    def rename_device(self, device_id: str, name: str) -> Dict[str, Any]:
        """Rename a device.
        
        Args:
            device_id: Device ID
            name: New device name
            
        Returns:
            Updated device information
        """
        try:
            data = {"name": name}
            response = self.session.put(
                f"{self.base_url}/devices/{device_id}",
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Renamed device {device_id} to {name}")
            return result
            
        except requests.RequestException as e:
            logger.error(f"Failed to rename device {device_id}: {e}")
            raise APIError(f"Failed to rename device: {e}")
    
    def get_device_events(
        self, 
        device_id: Optional[str] = None,
        event_prefix: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get events from device(s).
        
        Args:
            device_id: Specific device ID, or None for all devices
            event_prefix: Filter events by prefix
            
        Returns:
            List of events
        """
        try:
            url = f"{self.base_url}/events"
            if device_id:
                url += f"/{device_id}"
            if event_prefix:
                url += f"/{event_prefix}"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            # Note: Events endpoint returns server-sent events, 
            # this is a simplified version
            events = []
            for line in response.text.split('\n'):
                if line.startswith('data: '):
                    try:
                        import json
                        event_data = json.loads(line[6:])
                        events.append(event_data)
                    except json.JSONDecodeError:
                        continue
            
            logger.info(f"Retrieved {len(events)} events")
            return events
            
        except requests.RequestException as e:
            logger.error(f"Failed to get events: {e}")
            raise APIError(f"Failed to get events: {e}")
    
    def close(self):
        """Close the HTTP session."""
        if self.session:
            self.session.close()