# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-13T15:35:45.565043
- **Operation**: Operation failed - Visualization error
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **parameter**: None
- **node_id**: None
- **multi_param**: `["PUMP_V,INPUT_V"]`
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 6.6s
- **Error**: No valid data found for any of the specified measurements
- **Error Type**: Visualization error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "No valid data found for any of the specified measurements",
  "error_type": "Visualization error",
  "start_time": "2025-06-13T15:35:38.930629",
  "end_time": "2025-06-13T15:35:45.565037"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-13T15:35:45.565043",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/visualization/cli.py",
  "tool_name": "visualization",
  "environment_variables": {
    "CI": "false",
    "GITHUB_ACTIONS": "false",
    "GITHUB_ACTOR": null,
    "GITHUB_WORKFLOW": null,
    "GITHUB_RUN_ID": null,
    "MCP_SESSION": "false",
    "MCP_USER": null
  },
  "execution_source": "Manual/Local",
  "triggered_by": "zach@zach-Z390-AORUS-PRO-WIFI"
}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - visualization*
