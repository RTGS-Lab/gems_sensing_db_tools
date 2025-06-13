# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-13T15:36:37.881745
- **Operation**: Operation failed - Visualization error
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/parsed/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144_parsed_20250613_150955.csv
- **parameter**: INPUT_V
- **node_id**: None
- **multi_param**: None
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 0.3s
- **Error**: No data found for measurement 'INPUT_V'. Available measurements: PORT_1, PORT_2, PORT_3, START, STOP, Apogee, Clear, Red, Green, Blue, IR, ET, LE, H, VPD, PA, TA, RH, SAMP_CNT, AH, SVP, TD, DATA_QC
- **Error Type**: Visualization error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "No data found for measurement 'INPUT_V'. Available measurements: PORT_1, PORT_2, PORT_3, START, STOP, Apogee, Clear, Red, Green, Blue, IR, ET, LE, H, VPD, PA, TA, RH, SAMP_CNT, AH, SVP, TD, DATA_QC",
  "error_type": "Visualization error",
  "start_time": "2025-06-13T15:36:37.605184",
  "end_time": "2025-06-13T15:36:37.881737"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-13T15:36:37.881745",
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
