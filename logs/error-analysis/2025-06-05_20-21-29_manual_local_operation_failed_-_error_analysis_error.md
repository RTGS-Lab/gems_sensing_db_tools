# Error-Analysis Execution Log

## Execution Context
- **Timestamp**: 2025-06-05T20:21:29.308392
- **Operation**: Operation failed - Error analysis error
- **Execution Source**: Manual/Local
- **Triggered By**: zach@HEARTMACHINE
- **Hostname**: HEARTMACHINE
- **Platform**: Linux-6.11.0-26-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/Gems_Demo_2025-06-02_to_2025-06-05_20250605_201747.csv
- **error_column**: message
- **generate_graph**: False
- **node_filter**: all
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 0.0s
- **Error**: cannot import name 'load_data_file' from 'rtgs_lab_tools.device_monitoring.cli' (/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/device_monitoring/cli.py)
- **Error Type**: Error analysis error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "cannot import name 'load_data_file' from 'rtgs_lab_tools.device_monitoring.cli' (/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/device_monitoring/cli.py)",
  "error_type": "Error analysis error",
  "start_time": "2025-06-05T20:21:29.308372",
  "end_time": "2025-06-05T20:21:29.308388"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-05T20:21:29.308392",
  "user": "zach",
  "hostname": "HEARTMACHINE",
  "platform": "Linux-6.11.0-26-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/device_monitoring/cli.py",
  "tool_name": "error-analysis",
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
  "triggered_by": "zach@HEARTMACHINE"
}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - error-analysis*
