# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-13T15:46:28.648010
- **Operation**: Operation failed - Visualization error
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/LCCMR_Irrigation_2024-06-01_to_2024-09-30_20250610_124436.csv
- **parameter**: INPUT_V
- **node_id**: all
- **multi_param**: None
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 20.6s
- **Error**: No data found for measurement 'INPUT_V'. Available measurements: Time, Loc, Device ID, Packet ID, NumDevices, Devices, Apogee, Clear, Red, Green, Blue, IR, ET, LE, H, VPD, PA, TA, RH, SAMP_CNT, AH, SVP, TD, PARSING_ERROR, SD_Size, SD_Free, SD_SN, SD_MFG, SD_TYPE, Files, StackPointer, FRAM_Util, I2C_PORT_FAIL, PORT_V, PORT_I, ALPHA, ALPHA_INT, MUX, I2C_OB, I2C_1, I2C_2, I2C_3, I2C_4, Apogee_Type, Apogee_V, ADRs, Cycles, CellV, CellVAvg, CapLeft, CapTotal, TTF, SoC, Temperature, Accel_Offset, RTC_Config, AVG_P, LAST_CLR, ALS, ACCEL, SIV, FIX, Free Mem, Time Fix, Time Source, LOCAL, CELL, RTC, Last Sync, OB, Talon, I2C, INC, Adr, PUMP_V, PA_CELL, RH_CELL, TA_CELL, RH_ENCL, FLOW, INPUT_V, DATA_QC, TILT, GPS_RTC, TTFF, GPS
- **Error Type**: Visualization error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "No data found for measurement 'INPUT_V'. Available measurements: Time, Loc, Device ID, Packet ID, NumDevices, Devices, Apogee, Clear, Red, Green, Blue, IR, ET, LE, H, VPD, PA, TA, RH, SAMP_CNT, AH, SVP, TD, PARSING_ERROR, SD_Size, SD_Free, SD_SN, SD_MFG, SD_TYPE, Files, StackPointer, FRAM_Util, I2C_PORT_FAIL, PORT_V, PORT_I, ALPHA, ALPHA_INT, MUX, I2C_OB, I2C_1, I2C_2, I2C_3, I2C_4, Apogee_Type, Apogee_V, ADRs, Cycles, CellV, CellVAvg, CapLeft, CapTotal, TTF, SoC, Temperature, Accel_Offset, RTC_Config, AVG_P, LAST_CLR, ALS, ACCEL, SIV, FIX, Free Mem, Time Fix, Time Source, LOCAL, CELL, RTC, Last Sync, OB, Talon, I2C, INC, Adr, PUMP_V, PA_CELL, RH_CELL, TA_CELL, RH_ENCL, FLOW, INPUT_V, DATA_QC, TILT, GPS_RTC, TTFF, GPS",
  "error_type": "Visualization error",
  "start_time": "2025-06-13T15:46:08.059530",
  "end_time": "2025-06-13T15:46:28.648003"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-13T15:46:28.648010",
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
