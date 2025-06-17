# Data-Parser Execution Log

## Execution Context
- **Timestamp**: 2025-06-16T22:01:44.331020
- **Operation**: Parse GEMS data (all packets)
- **Execution Source**: Manual/Local
- **Triggered By**: zach@HEARTMACHINE
- **Hostname**: HEARTMACHINE
- **Platform**: Linux-6.11.0-26-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_records**: 29060
- **packet_types**: all
- **output_format**: csv
- **save_to_parsed_dir**: True
- **original_file_path**: data/LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250616_215805.csv

## Results Summary
- **Status**: ✅ Success
- **Duration**: 13.0s
- **Input Records**: 29060
- **Parsed Records**: 29060
- **Output Measurements**: 558170
- **Skipped Records**: 0
- **Packet Types**: all
- **Output File**: /home/zach/Code/rtgs-lab-tools/src/data/parsed/LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250616_215805_parsed_20250616_220135.csv

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "input_records": 29060,
  "parsed_records": 29060,
  "output_measurements": 558170,
  "skipped_records": 0,
  "packet_types": "all",
  "output_file": "/home/zach/Code/rtgs-lab-tools/src/data/parsed/LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250616_215805_parsed_20250616_220135.csv",
  "start_time": "2025-06-16T22:01:31.319379",
  "end_time": "2025-06-16T22:01:44.330997",
  "duration": 13.011618
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-16T22:01:44.331020",
  "user": "zach",
  "hostname": "HEARTMACHINE",
  "platform": "Linux-6.11.0-26-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/data_parser/core.py",
  "tool_name": "data-parser",
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
*Log generated automatically by RTGS Lab Tools - data-parser*
