#!/usr/bin/env python3
"""
Shared utilities for logging, config, dry-run support, timezone handling, and subprocess execution.
"""
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # Python 3.8 fallback (not needed for 3.12+)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", ".."))
SECRETS_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "secrets"))
TRACKING_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "data", "tracking"))

# EST/EDT timezone - automatically handles DST
EST_TZ = ZoneInfo("America/New_York")


def get_est_now() -> datetime:
    """
    Get current time in EST/EDT (America/New_York timezone).

    Returns:
        datetime: Timezone-aware datetime in EST/EDT
    """
    return datetime.now(EST_TZ)


def setup_logger(name: str, log_file: str | None = None, max_bytes: int = 5 * 1024 * 1024, backup_count: int = 5) -> logging.Logger:
    """
    Configure logger with rotating file handler and stdout.

    Args:
        name: Logger name
        log_file: Optional path to log file (enables file rotation)
        max_bytes: Max size per log file before rotation (default 5MB)
        backup_count: Number of rotated files to keep (default 5)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # Rotating file handler (if log_file specified)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger


def load_config(config_name: str) -> dict:
    """
    Load JSON config from scripts/ directory.

    Args:
        config_name: Config filename (e.g., "schedule-config.json")

    Returns:
        dict: Parsed config, empty dict if not found
    """
    path = os.path.join(SCRIPT_DIR, "..", config_name)
    path = os.path.normpath(path)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


# Dry-run support
DRY_RUN = "--dry-run" in sys.argv


def dry_run_check(action_description: str) -> bool:
    """
    Check if running in dry-run mode and print action if so.

    Args:
        action_description: Description of the action that would be taken

    Returns:
        bool: True if in dry-run mode (action should be skipped), False otherwise
    """
    if DRY_RUN:
        print(f"  🔍 DRY-RUN: {action_description}")
        return True
    return False


def run_subprocess_logged(
    cmd_list: list[str],
    logger: logging.Logger,
    timeout: int = 30,
    dry_run_check: bool = True,
) -> tuple[bool, str, str]:
    """
    Run a subprocess, capture stdout/stderr, and log results.

    Args:
        cmd_list: Command and arguments as list of strings
        logger: Logger instance for output
        timeout: Timeout in seconds (default 30)
        dry_run_check: Whether to check for --dry-run flag in sys.argv (default True)

    Returns:
        tuple: (success: bool, stdout: str, stderr: str)
    """
    # Check dry-run mode
    if dry_run_check and DRY_RUN:
        logger.info(f"DRY-RUN: would execute {' '.join(cmd_list)}")
        return True, "", ""

    cmd_str = " ".join(cmd_list)
    logger.debug(f"Executing: {cmd_str}")

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode == 0:
            if stdout:
                logger.info(f"Subprocess stdout: {stdout}")
            if stderr:
                logger.warning(f"Subprocess stderr: {stderr}")
            logger.info(f"Subprocess succeeded: {cmd_str}")
            return True, stdout, stderr
        else:
            if stdout:
                logger.debug(f"Subprocess stdout (exit={result.returncode}): {stdout}")
            if stderr:
                logger.error(f"Subprocess stderr (exit={result.returncode}): {stderr}")
            logger.error(f"Subprocess failed (exit={result.returncode}): {cmd_str}")
            return False, stdout, stderr

    except subprocess.TimeoutExpired:
        logger.error(f"Subprocess timed out after {timeout}s: {cmd_str}")
        return False, "", f"Timeout after {timeout} seconds"
    except FileNotFoundError:
        logger.error(f"Command not found: {cmd_list[0]}")
        return False, "", f"Command not found: {cmd_list[0]}"
    except Exception as e:
        logger.error(f"Subprocess error: {cmd_str} - {e}")
        return False, "", str(e)


__all__ = [
    "SCRIPT_DIR",
    "PROJECT_DIR",
    "SECRETS_DIR",
    "TRACKING_DIR",
    "EST_TZ",
    "get_est_now",
    "setup_logger",
    "load_config",
    "dry_run_check",
    "run_subprocess_logged",
    "DRY_RUN",
]