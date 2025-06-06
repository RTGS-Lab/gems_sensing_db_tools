# Data-Extraction Execution Log

## Execution Context
- **Timestamp**: 2025-06-05T19:57:48.129334
- **Operation**: Extract data from project 'Gems Demo' - Guadalupe device data extraction for error analysis - last 30 days
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@HEARTMACHINE
- **Hostname**: HEARTMACHINE
- **Platform**: Linux-6.11.0-26-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **project**: Gems Demo
- **start_date**: 2025-05-06
- **end_date**: 2025-06-05
- **node_ids**: `["e00fce6885951c63c0e86719"]`
- **output_format**: csv
- **output_directory**: /home/zach/Code/rtgs-lab-tools/data
- **create_zip**: False
- **retry_count**: 3
- **note**: Guadalupe device data extraction for error analysis - last 30 days

## Results Summary
- **Status**: ✅ Success
- **Duration**: 12.6s
- **Records Extracted**: 22743
- **Output File**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-05-06_to_2025-06-05_20250605_195747.csv

## Data Summary
- **Records**: 22743
- **Output**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-05-06_to_2025-06-05_20250605_195747.csv
- **Format**: CSV

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "records_extracted": 22743,
  "output_file": "/home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-05-06_to_2025-06-05_20250605_195747.csv",
  "start_time": "2025-06-05T19:57:35.578841",
  "end_time": "2025-06-05T19:57:48.129324"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-05T19:57:48.129334",
  "user": "zach",
  "hostname": "HEARTMACHINE",
  "platform": "Linux-6.11.0-26-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/sensing_data/cli.py",
  "tool_name": "data-extraction",
  "environment_variables": {
    "CI": "false",
    "GITHUB_ACTIONS": "false",
    "GITHUB_ACTOR": null,
    "GITHUB_WORKFLOW": null,
    "GITHUB_RUN_ID": null,
    "MCP_SESSION": "true",
    "MCP_USER": "claude"
  },
  "execution_source": "LLM/MCP",
  "triggered_by": "claude via zach@HEARTMACHINE"
}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - data-extraction*
