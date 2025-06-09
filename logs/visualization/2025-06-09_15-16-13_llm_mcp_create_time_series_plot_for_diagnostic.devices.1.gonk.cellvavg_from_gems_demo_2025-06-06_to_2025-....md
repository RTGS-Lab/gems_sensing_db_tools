# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-09T15:16:13.775905
- **Operation**: Create time series plot for Diagnostic.Devices.1.GONK.CellVAvg from Gems_Demo_2025-06-06_to_2025-06-09_20250609_151554.csv
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-06-06_to_2025-06-09_20250609_151554.csv
- **parameter**: Diagnostic.Devices.1.GONK.CellVAvg
- **node_id**: e00fce6885951c63c0e86719
- **multi_param**: None
- **output_dir**: figures
- **output_file**: None
- **format**: png
- **title**: Guadalupe Battery Voltage - Last 3 Days
- **show_markers**: True
- **note**: Battery voltage plot for Guadalupe device over the last 3 days

## Results Summary
- **Status**: ✅ Success
- **Duration**: 0.9s
- **Output File**: figures/Diagnostic_Devices_1_GONK_CellVAvg_timeseries.png
- **Records Processed**: 974
- **Note**: Battery voltage plot for Guadalupe device over the last 3 days

## Visualization Summary
- **Input**: /home/zach/Code/rtgs-lab-tools/data/Gems_Demo_2025-06-06_to_2025-06-09_20250609_151554.csv
- **Parameter: Diagnostic.Devices.1.GONK.CellVAvg**
- **Output**: figures/Diagnostic_Devices_1_GONK_CellVAvg_timeseries.png
- **Format**: PNG

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "output_file": "figures/Diagnostic_Devices_1_GONK_CellVAvg_timeseries.png",
  "records_processed": 974,
  "start_time": "2025-06-09T15:16:12.888960",
  "end_time": "2025-06-09T15:16:13.775895",
  "note": "Battery voltage plot for Guadalupe device over the last 3 days"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-09T15:16:13.775905",
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
