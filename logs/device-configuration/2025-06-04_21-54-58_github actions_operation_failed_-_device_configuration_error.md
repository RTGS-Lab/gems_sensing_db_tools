# Device-Configuration Execution Log

## Execution Context
- **Timestamp**: 2025-06-04T21:54:58.862822
- **Operation**: Operation failed - Device configuration error
- **Execution Source**: GitHub Actions
- **Triggered By**: zradlicz
- **Hostname**: pkrvmf6wy0o8zjz
- **Platform**: Linux-6.11.0-1014-azure-x86_64-with-glibc2.39
- **Working Directory**: /home/runner/work/rtgs-lab-tools/rtgs-lab-tools

## Parameters
- **config_source**: sensing_tools/device_configuration_updater/configurations/config.json
- **device_source**: sensing_tools/device_configuration_updater/e00fce6885951c63c0e86719
- **max_retries**: 3
- **note**: test guadalupe

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 0.0s
- **Error**: Configuration file not found: sensing_tools/device_configuration_updater/configurations/config.json
- **Error Type**: Device configuration error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "Configuration file not found: sensing_tools/device_configuration_updater/configurations/config.json",
  "error_type": "Device configuration error",
  "start_time": "2025-06-04T21:54:58.862539",
  "end_time": "2025-06-04T21:54:58.862814"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-04T21:54:58.862822",
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
    "GITHUB_RUN_ID": "15453545187",
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
