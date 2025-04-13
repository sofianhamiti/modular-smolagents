from smolagents.default_tools import Tool
import subprocess
from typing import Optional


class ExecuteCommandTool(Tool):
    name = "execute_command"
    description = "Runs a shell command and returns its output."
    inputs = {
        "command": {"type": "string", "description": "Shell command to execute."},
        "cwd": {
            "type": "string",
            "description": "Working directory (optional).",
            "nullable": True,
        },
        "timeout": {
            "type": "integer",
            "description": "Timeout in seconds (default: 30).",
            "nullable": True,
            "default": 30,
        },
    }
    output_type = "string"

    def forward(
        self, command: str, cwd: Optional[str] = None, timeout: int = 30
    ) -> str:
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            output = result.stdout.strip()
            error = result.stderr.strip()
            if result.returncode == 0:
                return output if output else "(No output)"
            else:
                return (
                    f"Command failed with code {result.returncode}:\n{error or output}"
                )
        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after {timeout} seconds."
        except Exception as e:
            return f"Error running command: {str(e)}"
