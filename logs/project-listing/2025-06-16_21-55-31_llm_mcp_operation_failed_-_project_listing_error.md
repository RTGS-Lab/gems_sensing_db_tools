# Project-Listing Execution Log

## Execution Context
- **Timestamp**: 2025-06-16T21:55:31.134630
- **Operation**: Operation failed - Project listing error
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@HEARTMACHINE
- **Hostname**: HEARTMACHINE
- **Platform**: Linux-6.11.0-26-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **note**: None

## Results Summary
- **Status**: ❌ Failed
- **Duration**: 2.2m
- **Error**: Failed to connect to database. Please check your configuration and VPN connection.
- **Error Type**: Project listing error

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "success": false,
  "error": "Failed to connect to database. Please check your configuration and VPN connection.",
  "error_type": "Project listing error",
  "start_time": "2025-06-16T21:53:17.957389",
  "end_time": "2025-06-16T21:55:31.134623"
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-16T21:55:31.134630",
  "user": "zach",
  "hostname": "HEARTMACHINE",
  "platform": "Linux-6.11.0-26-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/sensing_data/cli.py",
  "tool_name": "project-listing",
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
*Log generated automatically by RTGS Lab Tools - project-listing*
