# RTGS Lab Tools - Project Context

## Project Overview

**RTGS Lab Tools** is a Python package that consolidates environmental sensing data tools, gridded climate data access, IoT device management, and data visualization into a unified toolkit. The goal is to wrap all functionality in an MCP server for natural language interaction.

## IMPORTANT: Migration Requirements Update

### Critical Implementation Requirements

#### 1. Device Configuration Tool Fidelity
- **MUST** match the original `update_device_configurations.py` functionality exactly
- **MUST** maintain Git logging with automatic commit functionality
- **MUST** integrate with `.github/workflows/update_configuration.yaml` 
- **MUST** support file path arguments for config and device list locations
- **MUST** create detailed execution logs in markdown format for each run
- **MUST** preserve the GitLogger class and all audit trail functionality

#### 2. Self-Documenting Tools with Logs
- **ALL** tools must create a `logs/` folder in their respective directories
- **ALL** executions must generate timestamped log files similar to device_configuration_updater pattern
- **Format**: `YYYY-MM-DD_HH-MM-SS_[source]_[tool_name].md`
- **Content**: Execution context, parameters, results, duration, success/failure details

#### 3. MCP Server Implementation
- **MUST** use FastMCP framework (not the current server.py implementation)
- **MUST** follow the pattern established in `gems_sensing_db_tools_mcp_server.py`
- **MUST** call original scripts directly via subprocess (not reimplemented functions)
- **MUST** preserve all original CLI argument compatibility
- **MUST** maintain git logging and audit trails through MCP calls

## Current State

### Existing Code Structure
```
rtgs-lab-tools/
├── sensing_tools/
│   ├── device_data_getter/
│   │   └── get_sensing_data.py           # 400+ lines, needs refactoring
│   ├── time_series_visualizer/
│   │   └── gems_sensing_data_visualizer.py
│   ├── error_code_translator/
│   │   └── error_code_parser.py
│   └── device_configuration_updater/
│       ├── configuration_updater.py
│       └── uid_decoder.py
├── girdded_data_pullers/                 # Empty - new functionality
├── device_diagnostic_tools/              # Empty - future expansion
└── mcp_server/                          # Has basic implementation
```

### Key Components to Migrate
1. **get_sensing_data.py** - Main data extraction tool (most important)
2. **gems_sensing_data_visualizer.py** - Time series plotting
3. **error_code_parser.py** - Device error analysis
4. **configuration_updater.py** - Device configuration management
5. **uid_decoder.py** - Device UID utilities

## Target Structure

```
src/rtgs_lab_tools/
├── core/                    # Shared utilities
├── sensing_data/            # GEMS database tools
├── gridded_data/            # Climate data (ERA5, etc.)
├── visualization/           # Plotting tools
├── device_management/       # Particle device tools
└── mcp_server/             # Natural language interface
```

## Migration Strategy (UPDATED)

### Phase 1: Foundation ✅ COMPLETE
1. **Create package structure** with `pyproject.toml`
2. **Set up core utilities** (database, logging, config)
3. **Migrate sensing_data module** from `get_sensing_data.py`
4. **Basic MCP server** integration

### Phase 2: Full Migration ⚠️ NEEDS REVISION
1. Add gridded data capabilities (starting with ERA5) ✅
2. Migrate visualization and device management ⚠️ **PARTIAL - NEEDS FIX**
3. Complete MCP server with all tools ❌ **WRONG FRAMEWORK**

### Phase 3: Critical Fixes (NEW PRIORITY)
1. **Fix device updater** to match original functionality exactly
2. **Add git logging** to ALL tools with audit trails using core GitLogger class
3. **Reimplement MCP server** using FastMCP framework
4. **Add self-documenting logs** for each tool execution
5. **Ensure GitHub Actions compatibility** for all workflows

### Core GitLogger Implementation ✅
- **GitLogger class** extracted to `core/git_logger.py` for shared use
- **All tools** must use GitLogger for consistent audit trails
- **Execution context** detection (GitHub Actions, MCP, Manual)
- **Automatic git commits** with structured commit messages
- **Markdown logs** with execution context, parameters, and results

## Key Requirements

### Database Connection
- PostgreSQL database at `sensing-0.msi.umn.edu:5433`
- Requires UMN VPN connection
- Credentials in `.env` file

### API Integrations
- **Particle API**: Device management
- **Copernicus CDS**: ERA5 climate data
- **Various satellite APIs**: MODIS, Landsat, Sentinel

### Dependencies
- Core: `pandas`, `numpy`, `sqlalchemy`, `psycopg2-binary`
- Climate: `xarray`, `cdsapi`, `netcdf4`
- Visualization: `matplotlib`, `seaborn`, `plotly`
- MCP: `mcp[cli]`, `fastmcp`

## Code Style Guidelines

### Package Organization
- **CLI separation**: Keep CLI interfaces in `cli.py`, core logic in separate modules
- **Pure functions**: Business logic should be importable and testable
- **Shared utilities**: Common code goes in `core/` module
- **Error handling**: Custom exceptions in `core/exceptions.py`

### Naming Conventions
- **Package**: `rtgs_lab_tools`
- **CLI commands**: `rtgs-data`, `rtgs-era5`, `rtgs-visualize`
- **Functions**: Descriptive names like `get_raw_data()`, `pull_era5_data()`

### Function Signatures (REVISED APPROACH)
```python
# CORRECT - Keep original scripts, call via subprocess in MCP
# This preserves all functionality, git logging, and audit trails
async def get_raw_data_mcp(project: str, start_date: str, ...) -> Dict[str, Any]:
    """MCP wrapper that calls original get_sensing_data.py script."""
    cmd = [PYTHON_EXECUTABLE, "get_sensing_data.py", "--project", project, ...]
    stdout, stderr = await run_command(cmd)
    return {"output": stdout, "command": " ".join(cmd)}

# WRONG - Reimplementing breaks git logging and audit trails  
def get_raw_data(database_manager: DatabaseManager, ...) -> pd.DataFrame:
    """This approach loses the git logging and execution context."""
    pass
```

### Critical Implementation Pattern
```python
# Each tool MUST follow this pattern for MCP integration with GitLogger:
@mcp.tool("tool_name")
async def tool_name(...):
    # 1. Set MCP environment variables for git logging
    env = os.environ.copy()
    env['MCP_SESSION'] = 'true'
    env['MCP_USER'] = 'claude'
    
    # 2. Build command to call original script
    cmd = [PYTHON_EXECUTABLE, "original_script.py", ...]
    
    # 3. Run with environment for proper logging
    stdout, stderr = await run_command_with_env(cmd, env)
    
    # 4. Return structured response
    return {"output": stdout, "command": " ".join(cmd)}

# All CLI tools MUST use GitLogger for self-documenting execution:
from rtgs_lab_tools.core import GitLogger

def main():
    # Initialize git logger for this tool
    git_logger = GitLogger(tool_name="data-extraction")
    
    start_time = datetime.now()
    
    try:
        # Perform operation
        result = perform_operation(args)
        
        # Log successful execution
        git_logger.log_execution(
            operation=f"Extract data from {args.project}",
            parameters=vars(args),
            results={
                'success': True,
                'records_extracted': len(result),
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat()
            },
            script_path=__file__
        )
        
    except Exception as e:
        # Log failed execution
        git_logger.log_execution(
            operation=f"Extract data from {args.project}",
            parameters=vars(args),
            results={
                'success': False,
                'error': str(e),
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat()
            },
            script_path=__file__
        )
        raise
```

## MCP Integration Goals

### Target User Experience
```
Human: "Get temperature data from Winter Turf project for last month"

Claude: I'll extract the sensor data for you.
[Uses: get_sensing_data tool with project="Winter Turf", dates=last_month]

Result: Retrieved 5,247 records from 8 nodes
```

### Tool Categories
1. **Data Extraction**: `get_sensing_data`, `list_projects`
2. **Climate Data**: `download_era5_data`, `get_satellite_imagery`
3. **Visualization**: `create_time_series_plot`, `create_spatial_map`
4. **Device Management**: `list_devices`, `update_configuration`
5. **Analysis**: `analyze_error_codes`, `calculate_statistics`

## Current Challenges & Issues Identified

### Critical Issues with Current Migration
- **Device updater lacks git logging**: Current implementation missing GitLogger functionality
- **No self-documenting logs**: Tools don't create execution logs for audit trails
- **Wrong MCP framework**: Using mcp.server instead of FastMCP 
- **Function reimplementation**: Should call original scripts, not reimplement
- **Missing GitHub Actions integration**: Device updater not compatible with existing workflow
- **No file path arguments**: Can't specify config/device file locations

### Original Code Quality Issues (Still Valid)
- **Monolithic files**: `get_sensing_data.py` has 400+ lines mixing CLI, DB, and logic
- **Hardcoded values**: Database credentials, file paths scattered throughout
- **Poor error handling**: Generic try/catch blocks, unclear error messages
- **No testing**: Existing code lacks unit tests

### Missing Functionality (Updated)
- **Proper git logging**: All tools need audit trail like device_configuration_updater
- **Self-documenting execution**: Each tool run must create detailed logs
- **GitHub Actions compatibility**: All tools should work with existing workflows
- **Advanced visualization**: Interactive plots, web maps
- **Workflow automation**: Data pipelines, scheduled tasks

## Technical Specifications

### Database Schema (GEMS)
```sql
-- Main tables
raw           -- Raw sensor data (id, node_id, publish_time, message, etc.)
node          -- Node metadata (node_id, project, location, etc.)
parsed        -- Parsed sensor readings
```

### Configuration Format
```yaml
# .env file
DB_HOST=sensing-0.msi.umn.edu
DB_PORT=5433
DB_NAME=gems
DB_USER=username
DB_PASSWORD=password

# API keys
PARTICLE_ACCESS_TOKEN=token
CDS_API_KEY=key
```

### Output Formats
- **CSV**: Default for data exports
- **Parquet**: For large datasets
- **NetCDF**: For gridded climate data
- **GeoJSON**: For spatial data

## Development Workflow

### Setup Commands
```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/
```

### Testing Strategy
- **Unit tests**: Pure functions, isolated logic
- **Integration tests**: Database connections, API calls
- **MCP tests**: Tool execution, response formatting
- **Mock external services**: Database, APIs for testing

## Success Criteria (UPDATED)

### Phase 1 Complete ✅:
- [x] Package installs with `pip install rtgs-lab-tools`
- [x] `rtgs-data` command works (replaces `get_sensing_data.py`)
- [x] Core utilities (database, config, logging) are shared
- [x] Basic MCP server exposes sensing data tools
- [x] CI/CD pipeline runs tests automatically

### Phase 2 Partially Complete ⚠️:
- [x] ERA5 and satellite data access working
- [x] Visualization tools migrated
- ❌ Device management missing git logging
- ❌ MCP server using wrong framework
- ❌ No self-documenting logs

### Phase 3 Critical Fixes Required ❌:
- [ ] Device updater with FULL git logging functionality
- [ ] ALL tools create self-documenting logs in `logs/` folders
- [ ] MCP server rebuilt using FastMCP framework
- [ ] GitHub Actions workflow compatibility maintained
- [ ] File path arguments for config/device lists
- [ ] Execution audit trails for all tools

### Long-term Goals (Updated):
- [ ] All existing tools migrated with FULL original functionality
- [ ] Comprehensive audit trails and git logging for ALL tools
- [ ] Natural language interface via properly implemented FastMCP
- [ ] Published on PyPI for easy installation
- [ ] Full documentation and examples

## Notes for Claude Code (CRITICAL UPDATES)

### IMMEDIATE PRIORITIES:
1. **FIX Device Configuration Tool**: Must exactly match original `update_device_configurations.py`
2. **PRESERVE Git Logging**: GitLogger class and all audit functionality must remain
3. **IMPLEMENT FastMCP**: Replace current MCP server with FastMCP-based version
4. **ADD Self-Documenting Logs**: Every tool must create execution logs like device_configuration_updater
5. **MAINTAIN GitHub Actions**: Ensure all workflows continue to work

### Implementation Guidelines:
- **DO NOT reimplement existing scripts**: Call original scripts via subprocess
- **DO preserve all original CLI arguments**: Maintain full backward compatibility
- **DO add git logging to all tools**: Use pattern from device_configuration_updater
- **DO create logs/ folders**: Each tool directory needs timestamped execution logs
- **DO use FastMCP framework**: Follow gems_sensing_db_tools_mcp_server.py pattern
- **DO maintain file path arguments**: Config and device lists must be configurable

### Code Quality (Secondary):
- **Maintain backward compatibility**: Existing users should not be disrupted
- **Test everything**: New structure should be more testable than current code
- **Document decisions**: Explain why architectural choices were made

## Contact & Resources

- **Repository**: `https://github.com/RTGS-Lab/rtgs-lab-tools`
- **RTGS Lab**: `https://rtgs.umn.edu/`
- **Database Access**: Requires UMN VPN connection
- **API Documentation**: Copernicus CDS, Particle Cloud API docs