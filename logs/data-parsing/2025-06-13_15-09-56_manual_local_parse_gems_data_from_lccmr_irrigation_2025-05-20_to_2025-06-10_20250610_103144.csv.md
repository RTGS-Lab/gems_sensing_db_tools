# Data-Parsing Execution Log

## Execution Context
- **Timestamp**: 2025-06-13T15:09:56.371225
- **Operation**: Parse GEMS data from LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **output_format**: csv
- **packet_types**: data/v2
- **output_file**: /home/zach/Code/rtgs-lab-tools/data/parsed/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_150955.csv
- **note**: None

## Results Summary
- **Status**: ✅ Success
- **Duration**: 3.1s
- **Input Records**: 28389
- **Parsed Records**: 5729
- **Output Measurements**: 131377
- **Skipped Records**: 22660
- **Output File**: /home/zach/Code/rtgs-lab-tools/data/parsed/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_150955.csv
- **Note**: None

## Parsing Summary
- **Input Records**: 28389
- **Parsed Records**: 5729
- **Output Measurements**: 131377
- **Skipped Records**: 22660
- **Output File**: LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_150955.csv

## Packet Types
- **Filtered Types**: data/v2

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "input_records": 28389,
  "parsed_records": 5729,
  "output_measurements": 131377,
  "skipped_records": 22660,
  "output_file": "/home/zach/Code/rtgs-lab-tools/data/parsed/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_150955.csv",
  "start_time": "2025-06-13T15:09:53.236743",
  "end_time": "2025-06-13T15:09:56.371215",
  "note": null
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-13T15:09:56.371225",
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
