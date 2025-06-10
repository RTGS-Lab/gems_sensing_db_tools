# Error-Analysis Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T10:26:35.380549
- **Operation**: Analyze error codes from LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_095842.csv
- **Execution Source**: Manual/Local
- **Triggered By**: zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **input_file**: data/LCCMR_Irrigation_2025-05-20_to_2025-06-10_20250610_095842.csv
- **error_column**: message
- **generate_graph**: False
- **node_filter**: `["all"]`
- **output_dir**: figures
- **note**: None

## Results Summary
- **Status**: ✅ Success
- **Duration**: 1.6s
- **Total Errors Found**: 1446
- **Unique Error Codes**: 47
- **Plots Generated**: 0
- **Plot Files**: `[]`
- **Analysis File**: error test
- **Note**: None

## Error Analysis Summary
- **Total Errors**: 1446
- **Unique Codes**: 47
- **Plots Generated**: 0

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": true,
  "total_errors_found": 1446,
  "unique_error_codes": 47,
  "plots_generated": 0,
  "plot_files": [],
  "analysis_file": "error test",
  "start_time": "2025-06-10T10:26:33.817714",
  "end_time": "2025-06-10T10:26:35.380521",
  "note": null
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T10:26:35.380549",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/error_analysis/cli.py",
  "tool_name": "error-analysis",
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
*Log generated automatically by RTGS Lab Tools - error-analysis*
