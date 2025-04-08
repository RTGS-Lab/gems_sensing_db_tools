# GEMS Sensing Data Access Tool

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tool for extracting environmental sensor data from the GEMS database at the University of Minnesota.

## Overview

The GEMS Sensing Data Access Tool allows researchers to easily extract sensor data from the GEMS database by project, date range, and node IDs. It features robust error handling, data verification, and flexible output formats.

## Features

- Query sensor data by project name, date range, and specific nodes
- Export data in CSV or Parquet formats
- Compress outputs with metadata for archiving
- List available projects
- Verify data integrity through SHA-256 hashing
- Retry logic for handling network issues
- Detailed logging and verbose output options

## Installation

### Prerequisites
- Python 3.7+
- PostgreSQL client libraries (required for psycopg2)
- UMN VPN connection for database access

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sensing
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up credentials:
   ```bash
   python get_sensing_data.py --setup-credentials
   ```
   This will create a template `.env` file that you can edit with your database credentials.
   
   For credentials access, contact Bryan Runck (runck014@umn.edu).

5. Connect to UMN VPN:
   - Install the UMN VPN client from: https://it.umn.edu/services-technologies/virtual-private-network-vpn
   - Connect using your UMN credentials
   - The tool will not be able to access the database without an active VPN connection

## Usage

### Basic Command
```bash
python get_sensing_data.py --project "Winter Turf - v3" --start-date 2023-01-01 --end-date 2023-01-31
```

### Available Parameters
- `--project`: Project name to query (required)
- `--start-date`: Start date in YYYY-MM-DD format (default: 2018-01-01)
- `--end-date`: End date in YYYY-MM-DD format (default: today)
- `--node-id`: Specify one or more node IDs to query (comma-separated)
- `--output-dir`: Custom output directory for data files (default: ./data)
- `--output`: Specify output format: csv or parquet (default: csv)
- `--verbose`: Enable detailed output and data previews
- `--retry-count`: Maximum number of retry attempts (default: 3)
- `--zip`: Create a zip archive of the output files
- `--setup-credentials`: Create a template .env file for database credentials
- `--list-projects`: List all available projects and exit

## Examples

### List Available Projects
```bash
python get_sensing_data.py --list-projects
```

### Basic Data Extraction
```bash
python get_sensing_data.py --project "Winter Turf - v3" --start-date 2023-01-01 --end-date 2023-01-31
```

### Query Specific Node IDs
```bash
python get_sensing_data.py --project "Winter Turf - v3" --node-id node001,node002 --start-date 2023-01-01
```

### Create Compressed Output
```bash
python get_sensing_data.py --project "Winter Turf - v3" --start-date 2023-01-01 --end-date 2023-01-31 --zip
```

### Verbose Output with Custom Directory
```bash
python get_sensing_data.py --project "Winter Turf - v3" --start-date 2023-01-01 --verbose --output-dir /path/to/output
```

## Data Output

### Format
By default, the tool exports data as CSV files with the following characteristics:
- Located in a `/data` folder in the current directory (created if it doesn't exist)
- Named according to the pattern: `YYYYMMDDSTART_YYYYMMDDEND_project_CURRENTTIMESTAMP.csv` (or .parquet)
  (Example: `20230101_20230131_Winter Turf - v3_20240407153045.csv`)
- Includes file integrity verification using SHA-256 hashing
- Contains raw data records including node_id, event, message, and timestamps

### Compression Options
When using the `--zip` flag, the tool will:
- Create the CSV/parquet file as described above
- Compress the file into a zip archive with the same base name
- Include a metadata file in the archive with query details and statistics
- Provide a SHA-256 hash of the archive for verification

## Troubleshooting

### Database Connection Issues
If you encounter database connection errors, make sure:
1. You are connected to the UMN VPN
2. Your credentials in the `.env` file are correct
3. You have the appropriate permissions for the database

For VPN support, contact UMN Technology Help at 612-301-4357 or visit:
https://it.umn.edu/services-technologies/virtual-private-network-vpn

For database access, contact Bryan Runck at runck014@umn.edu

### Running Tests
To run the test suite:
```bash
cd tests
python run_tests.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact:
- Bryan Runck - runck014@umn.edu