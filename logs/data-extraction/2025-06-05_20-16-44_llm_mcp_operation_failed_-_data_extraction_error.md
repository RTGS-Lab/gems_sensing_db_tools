# Data-Extraction Execution Log

## Execution Context
- **Timestamp**: 2025-06-05T20:16:44.835219
- **Operation**: Operation failed - Data extraction error
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@HEARTMACHINE
- **Hostname**: HEARTMACHINE
- **Platform**: Linux-6.11.0-26-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **project**: Guadalupe
- **start_date**: 2025-06-02
- **end_date**: 2025-06-05
- **node_ids**: None
- **output_format**: csv
- **retry_count**: 3
- **note**: Data extraction for last 3 days as requested

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 0.1s
- **Error**: Project 'Guadalupe' not found. Available projects include:  (8 nodes), eROC (15 nodes), EROC MET Stations (12 nodes), Flight Demo (6 nodes), Flight Europe Demo (3 nodes), Gems demo (1 nodes), Gems Demo (20 nodes), GEMS DEMO (2 nodes), Irrigation (19 nodes), Irrigation Prototype (3 nodes), ... and 19 more projects with 395 nodes
- **Error Type**: Data extraction error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "Project 'Guadalupe' not found. Available projects include:  (8 nodes), eROC (15 nodes), EROC MET Stations (12 nodes), Flight Demo (6 nodes), Flight Europe Demo (3 nodes), Gems demo (1 nodes), Gems Demo (20 nodes), GEMS DEMO (2 nodes), Irrigation (19 nodes), Irrigation Prototype (3 nodes), ... and 19 more projects with 395 nodes",
  "error_type": "Data extraction error",
  "start_time": "2025-06-05T20:16:44.697390",
  "end_time": "2025-06-05T20:16:44.835198"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-05T20:16:44.835219",
  "user": "zach",
  "hostname": "HEARTMACHINE",
  "platform": "Linux-6.11.0-26-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/sensing_data/cli.py",
  "tool_name": "data-extraction",
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
  "triggered_by": "claude via zach@HEARTMACHINE"
}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - data-extraction*
