import logging
import time
import os
from typing import Optional

# Ensure the logs directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(log_dir, exist_ok=True)

# Absolute path for the log file
log_file = os.path.join(log_dir, "execution.log")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger("API")

def log_execution(
    func_name: str,
    success: bool,
    execution_time: Optional[float] = None,
    error: Optional[str] = None
):
    """Logs function execution details."""
    exec_time_str = f"{execution_time:.2f}ms" if execution_time else "N/A"
    
    if success:
        logger.info(f"EXECUTION_SUCCESS - Function: {func_name} | Time: {exec_time_str}")
    else:
        logger.error(f"EXECUTION_FAILED - Function: {func_name} | Error: {error} | Time: {exec_time_str}")
