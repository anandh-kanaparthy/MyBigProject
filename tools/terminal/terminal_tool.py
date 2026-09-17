from pathlib import Path
import subprocess


class TerminalTool:
    MAX_OUTPUT_SIZE = 50_000
    DEFAULT_TIMEOUT = 30

    BLOCKED_COMMANDS = {
        "format",
        "shutdown",
        "restart-computer",
        "stop-computer",
        "remove-item",
        "del",
        "erase",
        "rmdir",
        "rd",
    }

    def __init__(self, root_path):
        self.root_path = Path(root_path).resolve()

        if not self.root_path.exists():
            raise ValueError(f"Path does not exist: {self.root_path}")

        if not self.root_path.is_dir():
            raise ValueError(f"Path is not a directory: {self.root_path}")

    def _validate_command(self, command):
        if not command or not command.strip():
            raise ValueError("Command cannot be empty")

        command_lower = command.lower()

        for blocked in self.BLOCKED_COMMANDS:
            if blocked in command_lower:
                raise ValueError(
                    f"Blocked command detected: {blocked}"
                )

    def run(self, command, timeout=None):
        self._validate_command(command)

        timeout = timeout or self.DEFAULT_TIMEOUT

        try:
            result = subprocess.run(
                command,
                cwd=self.root_path,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "return_code": None,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds.",
            }

        stdout = result.stdout[:self.MAX_OUTPUT_SIZE]
        stderr = result.stderr[:self.MAX_OUTPUT_SIZE]

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": stdout,
            "stderr": stderr,
        }