# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T10:33:17.905081
- **Operation**: Create multi-parameter visualization from LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250610_103156.csv
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: /home/zach/Code/rtgs-lab-tools/data/LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250610_103156.csv
- **parameter**: None
- **node_id**: None
- **multi_param**: `["e00fce68f374e425e2d6b891,Diagnostic.Devices.0.LiCor ET.INPUT_V", "e00fce68f374e425e2d6b891,Diagnostic.Devices.1.LiCor ET.INPUT_V"]`
- **output_dir**: figures
- **output_file**: lccmr_047_input_v_summer_2024
- **format**: png
- **title**: LCCMR Device 47 INPUT_V - Summer 2024 (June 1 - August 31, 2024)
- **show_markers**: True
- **note**: INPUT_V visualization for LCCMR device 47 - summer 2024 data for comparison

## Results Summary
- **Status**: ✅ Success
- **Duration**: 15.3s
- **Output File**: figures/lccmr_047_input_v_summer_2024.png
- **Records Processed**: 29059
- **Note**: INPUT_V visualization for LCCMR device 47 - summer 2024 data for comparison

## Visualization Summary
- **Input**: /home/zach/Code/rtgs-lab-tools/data/LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250610_103156.csv
- **Multiple parameters: Diagnostic.Devices.0.LiCor ET.INPUT_V, Diagnostic.Devices.1.LiCor ET.INPUT_V**
- **Output**: figures/lccmr_047_input_v_summer_2024.png
- **Format**: PNG

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "output_file": "figures/lccmr_047_input_v_summer_2024.png",
  "records_processed": 29059,
  "start_time": "2025-06-10T10:33:02.628376",
  "end_time": "2025-06-10T10:33:17.905074",
  "note": "INPUT_V visualization for LCCMR device 47 - summer 2024 data for comparison"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T10:33:17.905081",
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
