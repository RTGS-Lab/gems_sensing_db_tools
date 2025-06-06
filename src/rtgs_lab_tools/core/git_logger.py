"""Git logging and audit trail functionality for RTGS Lab Tools."""

import getpass
import json
import logging
import os
import platform
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class GitLogger:
    """Handle git operations for logging tool executions with audit trails."""
    
    def __init__(self, tool_name: str, repo_path: Optional[str] = None):
        """Initialize GitLogger for a specific tool.
        
        Args:
            tool_name: Name of the tool (e.g., 'data-extraction', 'visualization', 'device-config')
            repo_path: Path to git repository root. If None, searches for .git directory.
        """
        self.tool_name = tool_name
        self.repo_path = repo_path or self._find_git_repo()
        self.logs_dir = Path(self.repo_path) / 'logs' / tool_name
        self.ensure_logs_directory()
        
    def _find_git_repo(self) -> str:
        """Find the git repository root by searching for .git directory."""
        current_dir = Path.cwd()
        
        # Search up the directory tree for .git
        for parent in [current_dir] + list(current_dir.parents):
            if (parent / '.git').exists():
                return str(parent)
        
        # If not found, use current directory
        logger.warning("Git repository not found, using current directory")
        return str(current_dir)
    
    def ensure_logs_directory(self):
        """Ensure the logs directory exists."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured logs directory exists: {self.logs_dir}")
        
    def _run_git_command(self, command: List[str], cwd: Optional[str] = None, input_text: str = None) -> Tuple[bool, str]:
        """Run a git command and return success status and output.
        
        Args:
            command: Git command as list of strings
            cwd: Working directory for command
            input_text: Optional input to pass to the command
            
        Returns:
            Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.repo_path,
                capture_output=True,
                text=True,
                input=input_text,
                timeout=30
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Git command timed out"
        except Exception as e:
            return False, f"Git command failed: {e}"
    
    def get_execution_context(self, script_path: Optional[str] = None) -> Dict[str, Any]:
        """Get context information about the current execution.
        
        Args:
            script_path: Path to the script being executed
            
        Returns:
            Dictionary with execution context information
        """
        context = {
            'timestamp': datetime.now().isoformat(),
            'user': getpass.getuser(),
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'working_directory': os.getcwd(),
            'script_path': script_path or 'unknown',
            'tool_name': self.tool_name,
            'environment_variables': {
                'CI': os.environ.get('CI', 'false'),
                'GITHUB_ACTIONS': os.environ.get('GITHUB_ACTIONS', 'false'),
                'GITHUB_ACTOR': os.environ.get('GITHUB_ACTOR'),
                'GITHUB_WORKFLOW': os.environ.get('GITHUB_WORKFLOW'),
                'GITHUB_RUN_ID': os.environ.get('GITHUB_RUN_ID'),
                'MCP_SESSION': os.environ.get('MCP_SESSION', 'false'),
                'MCP_USER': os.environ.get('MCP_USER')
            }
        }
        
        # Determine execution source
        if context['environment_variables']['GITHUB_ACTIONS'] == 'true':
            context['execution_source'] = 'GitHub Actions'
            context['triggered_by'] = context['environment_variables']['GITHUB_ACTOR']
        elif context['environment_variables']['MCP_SESSION'] == 'true':
            mcp_user = context['environment_variables']['MCP_USER'] or 'claude'
            context['execution_source'] = 'LLM/MCP'
            context['triggered_by'] = f"{mcp_user} via {context['user']}@{context['hostname']}"
        else:
            context['execution_source'] = 'Manual/Local'
            context['triggered_by'] = f"{context['user']}@{context['hostname']}"
            
        return context
    
    def create_execution_log(
        self,
        operation: str,
        parameters: Dict[str, Any],
        results: Dict[str, Any],
        script_path: Optional[str] = None,
        additional_sections: Optional[Dict[str, str]] = None
    ) -> str:
        """Create a detailed execution log file.
        
        Args:
            operation: Description of the operation performed
            parameters: Parameters used for the operation
            results: Results of the operation
            script_path: Path to the script that was executed
            additional_sections: Additional markdown sections to include
            
        Returns:
            Path to the created log file
        """
        context = self.get_execution_context(script_path)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        # Create safe filename from operation
        safe_operation = operation.lower().replace(' ', '_').replace('/', '_')
        log_filename = f"{timestamp}_{context['execution_source'].lower().replace('/', '_')}_{safe_operation}.md"
        log_path = self.logs_dir / log_filename
        
        # Calculate duration if available
        duration = self._calculate_duration(results)
        
        # Create log content
        log_content = f"""# {self.tool_name.title()} Execution Log

## Execution Context
- **Timestamp**: {context['timestamp']}
- **Operation**: {operation}
- **Execution Source**: {context['execution_source']}
- **Triggered By**: {context['triggered_by']}
- **Hostname**: {context['hostname']}
- **Platform**: {context['platform']}
- **Working Directory**: {context['working_directory']}

## Parameters
"""
        
        # Add parameters
        for key, value in parameters.items():
            if isinstance(value, (dict, list)):
                log_content += f"- **{key}**: `{json.dumps(value)}`\n"
            else:
                log_content += f"- **{key}**: {value}\n"
        
        # Add results summary
        log_content += f"""
## Results Summary
- **Status**: {'✅ Success' if results.get('success', True) else '❌ Failed'}
- **Duration**: {duration}
"""
        
        # Add specific result fields
        for key, value in results.items():
            if key not in ['success', 'start_time', 'end_time', 'duration']:
                if isinstance(value, (dict, list)):
                    log_content += f"- **{key.replace('_', ' ').title()}**: `{json.dumps(value)}`\n"
                else:
                    log_content += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        
        # Add additional sections if provided
        if additional_sections:
            for section_title, section_content in additional_sections.items():
                log_content += f"\n## {section_title}\n{section_content}\n"
        
        # Add detailed results
        log_content += f"""
## Detailed Results
<details>
<summary>Full Results JSON</summary>

```json
{json.dumps(results, indent=2)}
```
</details>

## Execution Environment
<details>
<summary>Environment Details</summary>

```json
{json.dumps(context, indent=2)}
```
</details>

---
*Log generated automatically by RTGS Lab Tools - {self.tool_name}*
"""
        
        # Write log file
        with open(log_path, 'w') as f:
            f.write(log_content)
            
        logger.info(f"Created execution log: {log_path}")
        return str(log_path)
    
    def _calculate_duration(self, results: Dict[str, Any]) -> str:
        """Calculate and format execution duration from results."""
        try:
            if 'start_time' in results and 'end_time' in results:
                start_time = datetime.fromisoformat(results['start_time'])
                end_time = datetime.fromisoformat(results['end_time'])
                duration = (end_time - start_time).total_seconds()
            elif 'duration' in results:
                duration = float(results['duration'])
            else:
                return "Unknown"
            
            if duration < 60:
                return f"{duration:.1f}s"
            elif duration < 3600:
                return f"{duration/60:.1f}m"
            else:
                return f"{duration/3600:.1f}h"
        except Exception:
            return "Unknown"
    
    def commit_and_push_log(self, log_path: str, operation: str, results: Dict[str, Any]) -> bool:
        """Commit and push the log file directly to the logs branch without checkout.
        
        This method uses git worktree to commit directly to the logs branch
        without affecting the current working directory or branch state.
        
        Args:
            log_path: Path to the log file
            operation: Description of the operation
            results: Results dictionary from the operation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure we're in a git repository
            success, _ = self._run_git_command(['git', 'status'])
            if not success:
                logger.warning("Not in a git repository, skipping log commit")
                return False
                
            # Ensure the log file exists
            if not os.path.exists(log_path):
                logger.error(f"Log file does not exist: {log_path}")
                return False
            
            # Create commit message with emoji based on success
            status_emoji = "✅" if results.get('success', False) else "❌"
            execution_source = self._get_execution_source()
            triggered_by = self._get_triggered_by()
            
            commit_message = f"{self.tool_name} log: {operation} {status_emoji} - {execution_source} by {triggered_by}"
            
            # Check if logs branch exists on remote and fetch it
            success, _ = self._run_git_command(['git', 'ls-remote', '--heads', 'origin', 'logs'])
            if success:
                # Fetch the remote logs branch
                self._run_git_command(['git', 'fetch', 'origin', 'logs:logs'])
            
            # Use a temporary worktree to commit to logs branch
            import tempfile
            import shutil
            
            with tempfile.TemporaryDirectory() as temp_dir:
                worktree_path = os.path.join(temp_dir, 'logs_worktree')
                
                # Create worktree for logs branch
                success, output = self._run_git_command(['git', 'worktree', 'add', worktree_path, 'logs'])
                if not success:
                    logger.warning(f"Failed to create worktree: {output}, committing to current branch")
                    # Fallback: just add and commit to current branch
                    success, _ = self._run_git_command(['git', 'add', log_path])
                    if success:
                        success, _ = self._run_git_command(['git', 'commit', '-m', commit_message])
                        if success:
                            self._run_git_command(['git', 'push'])
                    return success
                
                try:
                    # Copy log file to worktree
                    log_relative_path = os.path.relpath(log_path, self.repo_path)
                    target_path = os.path.join(worktree_path, log_relative_path)
                    
                    # Ensure target directory exists
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(log_path, target_path)
                    
                    # Add and commit in worktree
                    success, output = self._run_git_command(['git', 'add', log_relative_path], cwd=worktree_path)
                    if not success:
                        logger.error(f"Failed to add log file in worktree: {output}")
                        return False
                    
                    success, output = self._run_git_command(['git', 'commit', '-m', commit_message], cwd=worktree_path)
                    if not success:
                        logger.error(f"Failed to commit in worktree: {output}")
                        return False
                    
                    # Push from worktree
                    success, output = self._run_git_command(['git', 'push', 'origin', 'logs'], cwd=worktree_path)
                    if success:
                        logger.info(f"Successfully committed and pushed log: {commit_message}")
                        return True
                    else:
                        logger.warning(f"Failed to push logs branch: {output}")
                        logger.info(f"Successfully committed log locally: {commit_message}")
                        return True
                        
                finally:
                    # Clean up worktree
                    self._run_git_command(['git', 'worktree', 'remove', worktree_path])
                
        except Exception as e:
            logger.error(f"Failed to commit/push log: {e}")
            return False
    
    def log_execution(
        self,
        operation: str,
        parameters: Dict[str, Any],
        results: Dict[str, Any],
        script_path: Optional[str] = None,
        additional_sections: Optional[Dict[str, str]] = None,
        auto_commit: bool = True
    ) -> str:
        """Create execution log and optionally commit to git.
        
        This is a convenience method that combines create_execution_log and commit_and_push_log.
        
        Args:
            operation: Description of the operation performed
            parameters: Parameters used for the operation
            results: Results of the operation
            script_path: Path to the script that was executed
            additional_sections: Additional markdown sections to include
            auto_commit: Whether to automatically commit the log to git
            
        Returns:
            Path to the created log file
        """
        log_path = self.create_execution_log(
            operation=operation,
            parameters=parameters,
            results=results,
            script_path=script_path,
            additional_sections=additional_sections
        )
        
        if auto_commit:
            self.commit_and_push_log(log_path, operation, results)
        
        return log_path