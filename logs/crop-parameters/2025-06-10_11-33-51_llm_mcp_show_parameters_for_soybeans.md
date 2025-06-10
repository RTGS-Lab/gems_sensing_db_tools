# Crop-Parameters Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T11:33:51.085269
- **Operation**: Show parameters for soybeans
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **crop**: soybeans
- **note**: None

## Results Summary
- **Status**: ✅ Success
- **Duration**: Unknown
- **Crop**: soybeans
- **Parameters**: `{"tBase": 10.0, "tUpper": 30.0, "status": "verified", "verifiedBy": "Samikshya Subedi", "reference": "S.N., Edey. (1977). Growing degree-days and crop production in Canada. In Publication Agriculture Canada (Canada). no. 1635."}`

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "crop": "soybeans",
  "parameters": {
    "tBase": 10.0,
    "tUpper": 30.0,
    "status": "verified",
    "verifiedBy": "Samikshya Subedi",
    "reference": "S.N., Edey. (1977). Growing degree-days and crop production in Canada. In Publication Agriculture Canada (Canada). no. 1635."
  },
  "success": true
}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{
  "timestamp": "2025-06-10T11:33:51.085269",
  "user": "zach",
  "hostname": "zach-Z390-AORUS-PRO-WIFI",
  "platform": "Linux-6.11.0-25-generic-x86_64-with-glibc2.39",
  "python_version": "3.12.3",
  "working_directory": "/home/zach/Code/rtgs-lab-tools",
  "script_path": "/home/zach/Code/rtgs-lab-tools/src/rtgs_lab_tools/agricultural_modeling/cli.py",
  "tool_name": "crop-parameters",
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
*Log generated automatically by RTGS Lab Tools - crop-parameters*
