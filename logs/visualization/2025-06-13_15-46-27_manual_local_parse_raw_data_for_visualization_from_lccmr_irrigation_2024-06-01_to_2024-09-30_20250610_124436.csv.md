# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-13T15:46:27.644311
- **Operation**: Parse raw data for visualization from LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436.csv
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436.csv
- **packet_types**: all
- **purpose**: visualization preprocessing
- **saved_parsed_file**: /home/zach/Code/rtgs-lab-tools/data/parsed/LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436_parsed_20250613_154620.csv

## Results Summary
- **Status**: ✅ Success
- **Duration**: 19.6s
- **Input Records**: 36498
- **Parsed Records**: 36498
- **Output Measurements**: 696537
- **Skipped Records**: 0
- **Packet Types**: all
- **Parsed File Saved**: /home/zach/Code/rtgs-lab-tools/data/parsed/LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436_parsed_20250613_154620.csv

## Parsing Summary
- **Input Records**: 36498
- **Parsed Records**: 36498
- **Output Measurements**: 696537
- **Skipped Records**: 0
- **Saved File**: LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436_parsed_20250613_154620.csv

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "input_records": 36498,
  "parsed_records": 36498,
  "output_measurements": 696537,
  "skipped_records": 0,
  "packet_types": "all",
  "parsed_file_saved": "/home/zach/Code/rtgs-lab-tools/data/parsed/LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436_parsed_20250613_154620.csv",
  "start_time": "2025-06-13T15:46:08.059530",
  "end_time": "2025-06-13T15:46:27.644302"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-13T15:46:27.644311",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/visualization/data_utils.py",
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
