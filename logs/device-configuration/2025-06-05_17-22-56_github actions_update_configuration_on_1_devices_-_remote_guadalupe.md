# Device-Configuration Execution Log

## Execution Context
- **Timestamp**: 2025-06-05T17:22:56.070630
- **Operation**: Update configuration on 1 devices - remote guadalupe
- **Execution Source**: GitHub Actions
- **Triggered By**: zradlicz
- **Hostname**: pkrvmf6wy0o8zjz
- **Platform**: Linux-6.11.0-1014-azure-x86_64-with-glibc2.39
- **Working Directory**: /home/runner/work/rtgs-lab-tools/rtgs-lab-tools

## Parameters
- **config_source**: src/rtgs_lab_tools/device_configuration/configurations/config.json
- **device_source**: src/rtgs_lab_tools/device_configuration/devices/e00fce6885951c63c0e86719
- **total_devices**: 1
- **max_retries**: 3
- **restart_wait**: 30
- **online_timeout**: 120
- **max_concurrent**: 5
- **dry_run**: False
- **note**: remote guadalupe

## Results Summary
- **Status**: ✅ Success
- **Duration**: 1.1m
- **Total Devices**: 1
- **Successful Updates**: 1
- **Failed Updates**: 0
- **Success Rate**: 100.0
- **Output File**: ./update_results.json

## Update Summary
- **Successful**: 1/1 devices
- **Success Rate**: 100.0%
- **Expected System UID**: 59001428
- **Expected Sensor UID**: 1048576
- **Results**: ./update_results.json

## Device List
- ✅ `e00fce6885951c63c0e86719` - Success (System UID: 59001428, Sensor UID: 1048576)

## Configuration Applied
```json
{
  "config": {
    "system": {
      "logPeriod": 900,
      "backhaulCount": 4,
      "powerSaveMode": 2,
      "loggingMode": 2,
      "numAuxTalons": 1,
      "numI2CTalons": 1,
      "numSDI12Talons": 1
    },
    "sensors": {
      "numET": 0,
      "numHaar": 0,
      "numSoil": 1,
      "numApogeeSolar": 0,
      "numCO2": 0,
      "numO2": 0,
      "numPressure": 0
    }
  }
}
```

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "total_devices": 1,
  "successful_updates": 1,
  "failed_updates": 0,
  "success_rate": 100.0,
  "output_file": "./update_results.json",
  "start_time": "2025-06-05T17:21:52.836916",
  "end_time": "2025-06-05T17:22:56.070553"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-05T17:22:56.070630",
  "user": "runner",
  "hostname": "pkrvmf6wy0o8zjz",
  "platform": "Linux-6.11.0-1014-azure-x86_64-with-glibc2.39",
  "python_version": "3.12.10",
  "working_directory": "/home/runner/work/rtgs-lab-tools/rtgs-lab-tools",
  "script_path": "/home/runner/work/rtgs-lab-tools/rtgs-lab-tools/src/rtgs_lab_tools/device_configuration/cli.py",
  "tool_name": "device-configuration",
  "environment_variables": {
    "CI": "true",
    "GITHUB_ACTIONS": "true",
    "GITHUB_ACTOR": "zradlicz",
    "GITHUB_WORKFLOW": "Update Particle Device Configurations",
    "GITHUB_RUN_ID": "15473346826",
    "MCP_SESSION": "false",
    "MCP_USER": null
  },
  "execution_source": "GitHub Actions",
  "triggered_by": "zradlicz"
}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - device-configuration*
