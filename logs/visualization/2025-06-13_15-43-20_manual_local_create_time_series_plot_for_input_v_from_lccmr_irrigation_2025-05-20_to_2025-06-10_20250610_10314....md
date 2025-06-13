# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-13T15:43:20.799189
- **Operation**: Create time series plot for INPUT_V from LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **parameter**: INPUT_V
- **node_id**: None
- **multi_param**: None
- **output_dir**: figures
- **output_file**: None
- **format**: png
- **title**: None
- **show_markers**: True
- **note**: None

## Results Summary
- **Status**: ✅ Success
- **Duration**: 18.3s
- **Output File**: figures/INPUT_V_20250613_154319.png
- **Records Processed**: 599191
- **Note**: None

## Visualization Summary
- **Input**: data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **Measurement: INPUT_V**
- **Output**: figures/INPUT_V_20250613_154319.png
- **Format**: PNG

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "output_file": "figures/INPUT_V_20250613_154319.png",
  "records_processed": 599191,
  "start_time": "2025-06-13T15:43:02.542705",
  "end_time": "2025-06-13T15:43:20.799178",
  "note": null
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-13T15:43:20.799189",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/visualization/cli.py",
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
