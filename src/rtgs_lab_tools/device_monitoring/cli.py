#!/usr/bin/env python3
"""
CLI interface for GEMS error code analysis with GitLogger integration.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

import pandas as pd
import matplotlib.pyplot as plt

from ..core import GitLogger
from ..core.exceptions import ValidationError
from .error_parser import ErrorCodeParser, parse_error_codes, analyze_error_patterns

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_output_directory(output_dir: str = "figures") -> Path:
    """Ensure output directory exists."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def load_data_file(file_path: str) -> pd.DataFrame:
    """Load data from CSV or JSON file."""
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == '.csv':
        return pd.read_csv(file_path)
    elif file_ext == '.json':
        # Handle line-delimited JSON
        data = []
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    data.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        return pd.DataFrame(data)
    else:
        raise ValidationError(f"Unsupported file format: {file_ext}")


def filter_by_nodes(df: pd.DataFrame, node_filter: List[str]) -> pd.DataFrame:
    """Filter DataFrame by node IDs."""
    if not node_filter or 'all' in node_filter:
        return df
    
    if 'node_id' in df.columns:
        return df[df['node_id'].isin(node_filter)]
    else:
        logger.warning("No 'node_id' column found for filtering")
        return df


def create_error_frequency_plot(
    parsed_errors_df: pd.DataFrame, 
    output_dir: Path,
    node_id: Optional[str] = None
) -> str:
    """Create error frequency visualization."""
    if parsed_errors_df.empty:
        logger.warning("No errors to plot")
        return ""
    
    # Get top 15 most frequent errors
    error_counts = parsed_errors_df['normalized_code'].value_counts().head(15)
    
    if error_counts.empty:
        logger.warning("No error counts to plot")
        return ""
    
    # Create plot
    plt.figure(figsize=(16, 10))
    
    # Create bar plot
    bars = plt.bar(range(len(error_counts)), error_counts.values, color='royalblue', width=0.7)
    
    # Configure plot
    title = 'Error Code Frequency'
    if node_id and node_id != 'all':
        title += f' for Node {node_id}'
    
    plt.title(title, fontsize=18)
    plt.xlabel('Error Codes', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    
    # Set x-axis labels
    plt.xticks(range(len(error_counts)), error_counts.index, rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add count labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Add grid and formatting
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.subplots_adjust(bottom=0.15, left=0.1, right=0.95, top=0.9)
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"error_frequency_{node_id or 'all'}_{timestamp}.png"
    output_path = output_dir / filename
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Error frequency plot saved to {output_path}")
    return str(output_path)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Analyze GEMS device error codes")
    parser.add_argument("input_file", help="Path to CSV or JSON file containing error data")
    parser.add_argument("--output-dir", default="figures", help="Output directory for plots")
    parser.add_argument("--generate-graph", action="store_true", help="Generate error frequency graphs")
    parser.add_argument("--nodes", help="Comma-separated list of node IDs to analyze (use 'all' for all nodes)")
    parser.add_argument("--error-column", default="message", help="Column containing error data")
    parser.add_argument("--output-analysis", help="Save analysis results to JSON file")
    parser.add_argument("--no-git-log", action="store_true", help="Disable automatic git logging")
    parser.add_argument("--note", help="Description for this error analysis")
    
    args = parser.parse_args()
    
    # Initialize GitLogger
    git_logger = None
    if not args.no_git_log:
        try:
            git_logger = GitLogger(tool_name="error-analysis")
        except Exception as e:
            logger.warning(f"Failed to initialize git logging: {e}")
    
    start_time = datetime.now()
    
    try:
        # Load data
        logger.info(f"Loading data from {args.input_file}")
        df = load_data_file(args.input_file)
        logger.info(f"Loaded {len(df)} records")
        
        # Parse node filter
        node_filter = []
        if args.nodes:
            node_filter = [n.strip() for n in args.nodes.split(',')]
        
        # Filter by nodes if specified
        if node_filter and 'all' not in node_filter:
            df = filter_by_nodes(df, node_filter)
            logger.info(f"Filtered to {len(df)} records for nodes: {node_filter}")
        
        # Parse error codes
        logger.info("Parsing error codes...")
        parser = ErrorCodeParser()
        parsed_errors_df = parser.parse_error_codes_from_data(df, args.error_column)
        
        if parsed_errors_df.empty:
            logger.warning("No error codes found in the data")
            print("No error codes found in the input file.")
            return 0
        
        logger.info(f"Parsed {len(parsed_errors_df)} error instances")
        
        # Analyze error patterns
        analysis = analyze_error_patterns(parsed_errors_df)
        
        # Print summary
        print(f"\n=== ERROR ANALYSIS SUMMARY ===")
        print(f"Total Errors: {analysis['total_errors']}")
        print(f"Unique Error Codes: {analysis['unique_error_codes']}")
        print(f"Date Range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
        
        # Print top error codes
        print(f"\n=== TOP ERROR CODES ===")
        for i, error_info in enumerate(analysis['top_error_codes'], 1):
            print(f"{i}. {error_info['code']} ({error_info['count']}): {error_info['description']}")
        
        # Print errors by device
        if 'errors_by_device' in analysis:
            print(f"\n=== ERRORS BY DEVICE ===")
            for device, count in analysis['errors_by_device'].items():
                print(f"  {device}: {count}")
        
        # Print errors by node
        if 'errors_by_node' in analysis:
            print(f"\n=== ERRORS BY NODE ===")
            for node, count in list(analysis['errors_by_node'].items())[:10]:
                print(f"  {node}: {count}")
            if len(analysis['errors_by_node']) > 10:
                print(f"  ... and {len(analysis['errors_by_node']) - 10} more nodes")
        
        # Generate plots if requested
        output_dir = setup_output_directory(args.output_dir)
        plot_files = []
        
        if args.generate_graph:
            logger.info("Generating error frequency plots...")
            
            # Overall plot
            plot_file = create_error_frequency_plot(parsed_errors_df, output_dir, "all")
            if plot_file:
                plot_files.append(plot_file)
            
            # Per-node plots if filtering by specific nodes
            if node_filter and 'all' not in node_filter:
                for node_id in node_filter:
                    node_errors = parsed_errors_df[parsed_errors_df['node_id'] == node_id]
                    if not node_errors.empty:
                        plot_file = create_error_frequency_plot(node_errors, output_dir, node_id)
                        if plot_file:
                            plot_files.append(plot_file)
        
        # Save analysis results if requested
        if args.output_analysis:
            with open(args.output_analysis, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            logger.info(f"Analysis results saved to {args.output_analysis}")
        
        # Create git log if enabled
        if git_logger:
            try:
                operation = f"Analyze error codes from {Path(args.input_file).name}"
                if args.note:
                    operation += f" - {args.note}"
                
                parameters = {
                    'input_file': args.input_file,
                    'error_column': args.error_column,
                    'generate_graph': args.generate_graph,
                    'node_filter': node_filter,
                    'output_dir': args.output_dir,
                    'note': args.note
                }
                
                results = {
                    'success': True,
                    'total_errors_found': analysis['total_errors'],
                    'unique_error_codes': analysis['unique_error_codes'],
                    'plots_generated': len(plot_files),
                    'plot_files': plot_files,
                    'analysis_file': args.output_analysis,
                    'start_time': start_time.isoformat(),
                    'end_time': datetime.now().isoformat()
                }
                
                additional_sections = {
                    "Error Analysis Summary": f"- **Total Errors**: {analysis['total_errors']}\n- **Unique Codes**: {analysis['unique_error_codes']}\n- **Plots Generated**: {len(plot_files)}"
                }
                
                if plot_files:
                    additional_sections["Generated Plots"] = "\n".join([f"- {Path(p).name}" for p in plot_files])
                
                git_logger.log_execution(
                    operation=operation,
                    parameters=parameters,
                    results=results,
                    script_path=__file__,
                    additional_sections=additional_sections
                )
            except Exception as e:
                logger.error(f"Failed to create git log: {e}")
        
        return 0
        
    except Exception as e:
        error_msg = f"Error analysis failed: {e}"
        logger.error(error_msg)
        print(error_msg)
        
        # Log error to git if enabled
        if git_logger:
            try:
                operation = f"Error analysis failed - {type(e).__name__}"
                
                parameters = {
                    'input_file': args.input_file,
                    'error_column': args.error_column,
                    'note': args.note
                }
                
                results = {
                    'success': False,
                    'error': str(e),
                    'error_type': type(e).__name__,
                    'start_time': start_time.isoformat(),
                    'end_time': datetime.now().isoformat()
                }
                
                git_logger.log_execution(
                    operation=operation,
                    parameters=parameters,
                    results=results,
                    script_path=__file__
                )
            except Exception:
                pass  # Don't let git logging errors crash the application
        
        return 1


if __name__ == "__main__":
    sys.exit(main())