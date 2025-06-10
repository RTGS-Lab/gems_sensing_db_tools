# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T12:46:02.209821
- **Operation**: Create time series plot for Data.Devices.2.LiCor ET.TA from LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436.csv
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: /home/zach/Code/rtgs-lab-tools/data/LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436.csv
- **parameter**: Data.Devices.2.LiCor ET.TA
- **node_id**: e00fce68f374e425e2d6b891
- **multi_param**: None
- **output_dir**: figures
- **output_file**: None
- **format**: png
- **title**: LCCMR 47 Temperature Summer 2024
- **show_markers**: True
- **note**: Temperature data visualization for GDD calculation preparation

## Results Summary
- **Status**: ✅ Success
- **Duration**: 17.3s
- **Output File**: figures/Data_Devices_2_LiCor ET_TA_timeseries.png
- **Records Processed**: 36497
- **Note**: Temperature data visualization for GDD calculation preparation

## Visualization Summary
- **Input**: /home/zach/Code/rtgs-lab-tools/data/LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436.csv
- **Parameter: Data.Devices.2.LiCor ET.TA**
- **Output**: figures/Data_Devices_2_LiCor ET_TA_timeseries.png
- **Format**: PNG

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "output_file": "figures/Data_Devices_2_LiCor ET_TA_timeseries.png",
  "records_processed": 36497,
  "start_time": "2025-06-10T12:45:44.873167",
  "end_time": "2025-06-10T12:46:02.209813",
  "note": "Temperature data visualization for GDD calculation preparation"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T12:46:02.209821",
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
    "MCP_SESSION": "true",
    "MCP_USER": "claude"
  },
  "execution_source": "LLM/MCP",
  "triggered_by": "claude via zach@zach-Z390-AORUS-PRO-WIFI"
}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - visualization*
