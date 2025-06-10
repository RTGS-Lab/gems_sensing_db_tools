# Data-Extraction Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T09:30:11.178682
- **Operation**: Extract data from project 'Gems Demo'
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **success**: True
- **records_extracted**: 17107
- **output_file**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-06-03_to_2025-06-10_20250610_093010.csv
- **zip_file**: None
- **project**: Gems Demo
- **start_date**: 2025-06-03
- **end_date**: 2025-06-10
- **node_ids**: None
- **output_format**: csv
- **output_directory**: /home/zach/Code/rtgs-lab-tools/data
- **create_zip**: False
- **retry_count**: 3
- **note**: None

## Results Summary
- **Status**: ✅ Success
- **Duration**: 4.1s
- **Records Extracted**: 17107
- **Output File**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-06-03_to_2025-06-10_20250610_093010.csv
- **Note**: None

## Data Summary
- **Records**: 17107
- **Output**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-06-03_to_2025-06-10_20250610_093010.csv
- **Format**: CSV

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "records_extracted": 17107,
  "output_file": "/home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-06-03_to_2025-06-10_20250610_093010.csv",
  "start_time": "2025-06-10T09:30:07.118263",
  "end_time": "2025-06-10T09:30:11.178673",
  "note": null
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T09:30:11.178682",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
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
