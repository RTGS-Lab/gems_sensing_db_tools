# Visualization Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T10:32:53.763904
- **Operation**: Create multi-parameter visualization from LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: /home/zach/Code/rtgs-lab-tools/data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **parameter**: None
- **node_id**: None
- **multi_param**: `["e00fce68f374e425e2d6b891,Diagnostic.Devices.0.LiCor ET.INPUT_V", "e00fce68f374e425e2d6b891,Diagnostic.Devices.1.LiCor ET.INPUT_V"]`
- **output_dir**: figures
- **output_file**: lccmr_047_input_v_recent_3weeks
- **format**: png
- **title**: LCCMR Device 47 INPUT_V - Last 3 Weeks (May 20 - June 10, 2025)
- **show_markers**: True
- **note**: INPUT_V visualization for LCCMR device 47 - recent 3 weeks data

## Results Summary
- **Status**: ✅ Success
- **Duration**: 14.7s
- **Output File**: figures/lccmr_047_input_v_recent_3weeks.png
- **Records Processed**: 28389
- **Note**: INPUT_V visualization for LCCMR device 47 - recent 3 weeks data

## Visualization Summary
- **Input**: /home/zach/Code/rtgs-lab-tools/data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_103144.csv
- **Multiple parameters: Diagnostic.Devices.0.LiCor ET.INPUT_V, Diagnostic.Devices.1.LiCor ET.INPUT_V**
- **Output**: figures/lccmr_047_input_v_recent_3weeks.png
- **Format**: PNG

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "output_file": "figures/lccmr_047_input_v_recent_3weeks.png",
  "records_processed": 28389,
  "start_time": "2025-06-10T10:32:39.077168",
  "end_time": "2025-06-10T10:32:53.763897",
  "note": "INPUT_V visualization for LCCMR device 47 - recent 3 weeks data"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T10:32:53.763904",
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
