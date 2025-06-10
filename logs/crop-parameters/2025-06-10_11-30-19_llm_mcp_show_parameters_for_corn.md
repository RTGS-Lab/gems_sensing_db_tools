# Crop-Parameters Execution Log

## Execution Context
- **Timestamp**: 2025-06-10T11:30:19.877290
- **Operation**: Show parameters for corn
- **Execution Source**: LLM/MCP
- **Triggered By**: claude via zach@zach-Z390-AORUS-PRO-WIFI
- **Hostname**: zach-Z390-AORUS-PRO-WIFI
- **Platform**: Linux-6.11.0-25-generic-x86_64-with-glibc2.39
- **Working Directory**: /home/zach/Code/rtgs-lab-tools

## Parameters
- **crop**: corn
- **note**: None

## Results Summary
- **Status**: ✅ Success
- **Duration**: Unknown
- **Crop**: corn
- **Parameters**: `{"tBase": 10.0, "tUpper": 30.0, "status": "verified", "verifiedBy": "Samikshya Subedi", "reference": "Darby, H. M., & Lauer, J. G. (2002). Harvest date and hybrid influence on corn forage yield, quality, and preservation. Agronomy Journal, 94(3), 559\u2013566."}`

## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{
  "crop": "corn",
  "parameters": {
    "tBase": 10.0,
    "tUpper": 30.0,
    "status": "verified",
    "verifiedBy": "Samikshya Subedi",
    "reference": "Darby, H. M., & Lauer, J. G. (2002). Harvest date and hybrid influence on corn forage yield, quality, and preservation. Agronomy Journal, 94(3), 559\u2013566."
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
  "timestamp": "2025-06-10T11:30:19.877290",
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
