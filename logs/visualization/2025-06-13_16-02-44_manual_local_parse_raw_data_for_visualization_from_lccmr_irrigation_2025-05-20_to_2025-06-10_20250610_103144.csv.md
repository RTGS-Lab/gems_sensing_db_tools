# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-13T16:02:44.885133
- **Operation**: Parse raw data for visualization from LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **packet_types**: all
- **purpose**: visualization preprocessing
- **saved_parsed_file**: /home/zach/Code/rtgs-lab-tools/src/data/parsed/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_160231.csv

## Results Summary
- **Status**: ✅ Success
- **Duration**: 20.9s
- **Input Records**: 28389
- **Parsed Records**: 28389
- **Output Measurements**: 599191
- **Skipped Records**: 0
- **Packet Types**: all
- **Output File**: /home/zach/Code/rtgs-lab-tools/src/data/parsed/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_160231.csv

## Parsing Summary
- **Input Records**: 28389
- **Parsed Records**: 28389
- **Output Measurements**: 599191
- **Skipped Records**: 0
- **Saved File**: LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_160231.csv

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "input_records": 28389,
  "parsed_records": 28389,
  "output_measurements": 599191,
  "skipped_records": 0,
  "packet_types": "all",
  "output_file": "/home/zach/Code/rtgs-lab-tools/src/data/parsed/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_160231.csv",
  "start_time": "2025-06-13T16:02:23.949477",
  "end_time": "2025-06-13T16:02:44.885123"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-13T16:02:44.885133",
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
