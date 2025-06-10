# Data-Extraction Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T09:46:47.907927
- **Operation**: Operation failed - Data extraction error
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **project**: lccmr
- **start_date**: 2025-05-20
- **end_date**: 2025-06-10
- **node_ids**: e00fce68f374e425e2d6b891
- **output_format**: csv
- **retry_count**: 3
- **note**: LCCMR device 47 data for last 3 weeks - INPUT_V analysis

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 0.1s
- **Error**: Project 'lccmr' not found. Available projects include:  (8 nodes), eROC (15 nodes), EROC MET Stations (12 nodes), Flight Demo (6 nodes), Flight Europe Demo (3 nodes), Gems demo (1 nodes), Gems Demo (20 nodes), GEMS DEMO (2 nodes), Irrigation (19 nodes), Irrigation Prototype (3 nodes), ... and 20 more projects with 397 nodes
- **Error Type**: Data extraction error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "Project 'lccmr' not found. Available projects include:  (8 nodes), eROC (15 nodes), EROC MET Stations (12 nodes), Flight Demo (6 nodes), Flight Europe Demo (3 nodes), Gems demo (1 nodes), Gems Demo (20 nodes), GEMS DEMO (2 nodes), Irrigation (19 nodes), Irrigation Prototype (3 nodes), ... and 20 more projects with 397 nodes",
  "error_type": "Data extraction error",
  "start_time": "2025-06-10T09:46:47.797975",
  "end_time": "2025-06-10T09:46:47.907919"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T09:46:47.907927",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
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
  "triggered_by": "claude via zach@zach-Z390-AORUS-PRO-WIFI"
}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - data-extraction*
