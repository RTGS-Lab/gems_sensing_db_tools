# Data-Extraction Execution Log

## Execution Context
- **Timestamp**: 2025-06-04T11:38:27.633649
- **Operation**: Data extraction failed - Configuration error
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/gems_sensing_db_tools/src/rtgs_lab_tools/mcp_server

## Parameters
- **project**: None
- **start_date**: 2018-01-01
- **end_date**: None
- **node_id**: None
- **output**: csv
- **retry_count**: 3
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 0.0s
- **Error**: DB_USER not found in environment variables
- **Error Type**: Configuration error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "DB_USER not found in environment variables",
  "error_type": "Configuration error",
  "start_time": "2025-06-04T11:38:27.633493",
  "end_time": "2025-06-04T11:38:27.633645"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-04T11:38:27.633649",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/gems_sensing_db_tools/src/rtgs_lab_tools/mcp_server",
  "script_path": "/home/zach/Code/gems_sensing_db_tools/src/rtgs_lab_tools/cli.py",
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
