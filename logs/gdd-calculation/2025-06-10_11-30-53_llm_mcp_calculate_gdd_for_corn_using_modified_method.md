# Gdd-Calculation Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T11:30:53.704153
- **Operation**: Calculate GDD for corn using modified method
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **t_min**: 15.5
- **t_max**: 28.3
- **crop**: corn
- **method**: modified
- **t_base**: 10.0
- **t_upper**: 30.0
- **note**: Example GDD calculation for corn

## Results Summary
- **Status**: ✅ Success
- **Duration**: Unknown
- **Gdd**: 11.899999999999999

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "gdd": 11.899999999999999,
  "success": true
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T11:30:53.704153",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/agricultural_modeling/cli.py",
  "tool_name": "gdd-calculation",
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
*Log generated automatically by RTGS Lab Tools - gdd-calculation*
