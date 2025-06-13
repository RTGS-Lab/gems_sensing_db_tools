# Data-Parsing Execution Log

## Execution Context
- **Timestamp**: 2025-06-13T14:23:30.881635
- **Operation**: Operation failed - Data parsing error
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **output_format**: csv
- **packet_types**: data/v2
- **output_file**: None
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 1.9s
- **Error**: The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
- **Error Type**: Data parsing error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().",
  "error_type": "Data parsing error",
  "start_time": "2025-06-13T14:23:29.000435",
  "end_time": "2025-06-13T14:23:30.881630"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-13T14:23:30.881635",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/data_parser/cli.py",
  "tool_name": "data-parsing",
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
*Log generated automatically by RTGS Lab Tools - data-parsing*
