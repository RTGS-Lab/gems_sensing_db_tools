# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T10:00:18.373294
- **Operation**: Create multi-parameter visualization from LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250610_095859.csv
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: /home/zach/Code/rtgs-lab-tools/data/LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250610_095859.csv
- **parameter**: None
- **node_id**: None
- **multi_param**: `["e00fce68f374e425e2d6b891,Diagnostic.Devices.0.LiCor ET.INPUT_V", "e00fce68f374e425e2d6b891,Diagnostic.Devices.1.LiCor ET.INPUT_V"]`
- **output_dir**: figures
- **output_file**: LCCMR_047_INPUT_V_summer_2024
- **format**: png
- **title**: LCCMR_047 INPUT_V - Summer 2024 (June - August)
- **show_markers**: True
- **note**: INPUT_V visualization for LCCMR device 47 - summer 2024

## Results Summary
- **Status**: ✅ Success
- **Duration**: 15.0s
- **Output File**: figures/LCCMR_047_INPUT_V_summer_2024.png
- **Records Processed**: 29059
- **Note**: INPUT_V visualization for LCCMR device 47 - summer 2024

## Visualization Summary
- **Input**: /home/zach/Code/rtgs-lab-tools/data/LCCMR_Irrigation_2024-06-01_to_2024-08-31_20250610_095859.csv
- **Multiple parameters: Diagnostic.Devices.0.LiCor ET.INPUT_V, Diagnostic.Devices.1.LiCor ET.INPUT_V**
- **Output**: figures/LCCMR_047_INPUT_V_summer_2024.png
- **Format**: PNG

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "output_file": "figures/LCCMR_047_INPUT_V_summer_2024.png",
  "records_processed": 29059,
  "start_time": "2025-06-10T10:00:03.336053",
  "end_time": "2025-06-10T10:00:18.373286",
  "note": "INPUT_V visualization for LCCMR device 47 - summer 2024"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T10:00:18.373294",
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
