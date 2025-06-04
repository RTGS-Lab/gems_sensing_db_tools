# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-04T10:34:42.371771
- **Operation**: Create time series plot for Diagnostic.Devices.1.GONK.CellV from Gems_Demo_2025-06-03_to_2025-06-04_20250604_102718.csv
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/gems_sensing_db_tools

## Parameters
- **input_file**: Gems_Demo_2025-06-03_to_2025-06-04_20250604_102718.csv
- **parameter**: Diagnostic.Devices.1.GONK.CellV
- **node_id**: e00fce6885951c63c0e86719
- **multi_param**: None
- **output_dir**: figures
- **output_file**: None
- **format**: png
- **title**: None
- **show_markers**: True
- **note**: None

## Results Summary
- **Status**: ✅ Success
- **Duration**: 2.1s
- **Output File**: figures/Diagnostic_Devices_1_GONK_CellV_timeseries.png
- **Records Processed**: 2095

## Visualization Summary
- **Input**: Gems_Demo_2025-06-03_to_2025-06-04_20250604_102718.csv
- **Parameter: Diagnostic.Devices.1.GONK.CellV**
- **Output**: figures/Diagnostic_Devices_1_GONK_CellV_timeseries.png
- **Format**: PNG

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "output_file": "figures/Diagnostic_Devices_1_GONK_CellV_timeseries.png",
  "records_processed": 2095,
  "start_time": "2025-06-04T10:34:40.297453",
  "end_time": "2025-06-04T10:34:42.371761"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-04T10:34:42.371771",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/gems_sensing_db_tools",
  "script_path": "/home/zach/Code/gems_sensing_db_tools/src/rtgs_lab_tools/cli.py",
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
