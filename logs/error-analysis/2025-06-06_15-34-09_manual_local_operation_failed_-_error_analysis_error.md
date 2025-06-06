# Error-Analysis Execution Log

## Execution Context
- **Timestamp**: 2025-06-06T15:34:09.504894
- **Operation**: Operation failed - Error analysis error
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/Gems_Demo_2025-06-03_to_2025-06-06_20250606_124931.csv
- **error_column**: message
- **generate_graph**: False
- **node_filter**: None
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 0.0s
- **Error**: Data file not found: data/Gems_Demo_2025-06-03_to_2025-06-06_20250606_124931.csv
- **Error Type**: Error analysis error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "Data file not found: data/Gems_Demo_2025-06-03_to_2025-06-06_20250606_124931.csv",
  "error_type": "Error analysis error",
  "start_time": "2025-06-06T15:34:09.504779",
  "end_time": "2025-06-06T15:34:09.504889"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-06T15:34:09.504894",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/error_analysis/cli.py",
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
  "triggered_by": "zach@zach-Z390-AORUS-PRO-WIFI"
}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - error-analysis*
