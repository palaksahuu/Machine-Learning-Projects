import os
import webbrowser
import psutil
import subprocess
from typing import Dict, Union

def open_chrome() -> None:
    """Opens Google Chrome browser. Returns None."""
    webbrowser.open("https://www.google.com")

def open_calculator() -> None:
    """Launches system calculator. Returns None."""
    os.system("calc" if os.name == 'nt' else "gnome-calculator")

def get_cpu_usage() -> float:
    """Returns current CPU usage percentage (0-100)."""
    return psutil.cpu_percent(interval=1)

def run_shell_command(command: str) -> Dict[str, Union[str, int]]:
    """
    Executes a shell command.
    Args:
        command: Shell command string
    Returns:
        Dictionary with stdout, stderr, and returncode
    """
    result = subprocess.run(
        command, 
        shell=True, 
        capture_output=True, 
        text=True
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }