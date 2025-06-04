# Data-Extraction Execution Log

## Execution Context
- **Timestamp**: 2025-06-04T10:27:18.275560
- **Operation**: Extract data from project 'Gems Demo'
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/gems_sensing_db_tools

## Parameters
- **project**: Gems Demo
- **start_date**: 2025-06-03
- **end_date**: 2025-06-04
- **node_ids**: None
- **output_format**: csv
- **output_directory**: /home/zach/Code/gems_sensing_db_tools
- **create_zip**: False
- **retry_count**: 3
- **note**: None

## Results Summary
- **Status**: ✅ Success
- **Duration**: 4.6s
- **Records Extracted**: 2187
- **Output File**: /home/zach/Code/gems_sensing_db_tools/Gems_Demo_2025-06-03_to_2025-06-04_20250604_102718.csv

## Data Summary
- **Records**: 2187
- **Output**: /home/zach/Code/gems_sensing_db_tools/Gems_Demo_2025-06-03_to_2025-06-04_20250604_102718.csv
- **Format**: CSV

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "records_extracted": 2187,
  "output_file": "/home/zach/Code/gems_sensing_db_tools/Gems_Demo_2025-06-03_to_2025-06-04_20250604_102718.csv",
  "start_time": "2025-06-04T10:27:13.642879",
  "end_time": "2025-06-04T10:27:18.275552"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-04T10:27:18.275560",
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
