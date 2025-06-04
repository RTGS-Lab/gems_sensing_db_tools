# Data-Extraction Execution Log

## Execution Context
- **Timestamp**: 2025-06-04T10:25:58.589457
- **Operation**: Data extraction failed - Application error
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/gems_sensing_db_tools

## Parameters
- **project**: Gems Demo
- **start_date**: 06-03-2025
- **end_date**: 2025-06-04
- **node_id**: None
- **output**: csv
- **retry_count**: 3
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 0.1s
- **Error**: Invalid date format: time data '06-03-2025' does not match format '%Y-%m-%d'
- **Error Type**: Application error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "Invalid date format: time data '06-03-2025' does not match format '%Y-%m-%d'",
  "error_type": "Application error",
  "start_time": "2025-06-04T10:25:58.502735",
  "end_time": "2025-06-04T10:25:58.589450"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-04T10:25:58.589457",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/gems_sensing_db_tools",
  "script_path": "/home/zach/Code/gems_sensing_db_tools/src/rtgs_lab_tools/cli.py",
  "tool_name": "data-extraction",
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
*Log generated automatically by RTGS Lab Tools - data-extraction*
