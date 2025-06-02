# GEMS Sentinel

GEMS Sentinel is a fully autonomous monitoring and alerting tool for the GEMS v3 sensing device fleet. This system proactively identifies device failures, system anomalies, and critical battery issues without human intervention.

## Features

- Runs daily (or configurable) to check device health
- Monitors:
  - Battery voltage (<3.6V warning, <3.2V critical)
  - System usage based on [GEMS Power Mode Docs](https://github.com/RTGS-Lab/GEMS-v3-Power-Mode-Documentation)
  - Error codes based on [ERRORCODES.md](https://github.com/RTGS-Lab/Firmware_-_FlightControl-Demo/blob/master/ERRORCODES.md)
  - Sensor dropouts or inactive data streams
- Sends live alerts via email or app:
  - Graphs of relevant metrics over time
  - Synopsis of detected issue
  - Suggested fixes
- Categorizes issues by severity
- Tracks trends over time for each device

## Vision

> *"I know you're out there. I can feel you now. I know that you're afraid... you're afraid of us."* — *Neo*
