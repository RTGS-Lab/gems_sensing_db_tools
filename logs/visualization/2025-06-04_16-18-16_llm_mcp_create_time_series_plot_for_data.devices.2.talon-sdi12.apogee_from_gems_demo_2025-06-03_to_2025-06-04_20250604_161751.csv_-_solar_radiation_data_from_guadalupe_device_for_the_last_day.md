# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-04T16:18:16.868900
- **Operation**: Create time series plot for Data.Devices.2.Talon-SDI12.Apogee from Gems_Demo_2025-06-03_to_2025-06-04_20250604_161751.csv - Solar radiation data from Guadalupe device for the last day
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-06-03_to_2025-06-04_20250604_161751.csv
- **parameter**: Data.Devices.2.Talon-SDI12.Apogee
- **node_id**: e00fce6885951c63c0e86719
- **multi_param**: None
- **output_dir**: figures
- **output_file**: None
- **format**: png
- **title**: Guadalupe Solar Radiation - Last 24 Hours
- **show_markers**: True
- **note**: Solar radiation data from Guadalupe device for the last day

## Results Summary
- **Status**: ✅ Success
- **Duration**: 1.3s
- **Output File**: figures/Data_Devices_2_Talon-SDI12_Apogee_timeseries.png
- **Records Processed**: 2095

## Visualization Summary
- **Input**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-06-03_to_2025-06-04_20250604_161751.csv
- **Parameter: Data.Devices.2.Talon-SDI12.Apogee**
- **Output**: figures/Data_Devices_2_Talon-SDI12_Apogee_timeseries.png
- **Format**: PNG

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "output_file": "figures/Data_Devices_2_Talon-SDI12_Apogee_timeseries.png",
  "records_processed": 2095,
  "start_time": "2025-06-04T16:18:15.524643",
  "end_time": "2025-06-04T16:18:16.868891"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-04T16:18:16.868900",
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
