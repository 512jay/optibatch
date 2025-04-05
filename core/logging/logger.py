# core/logging/logger.py

from loguru import logger
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.add(
    LOG_DIR / "optibach.log",
    rotation="1 MB",  # Rotate after 1MB
    retention="7 days",  # Keep logs for 1 week
    compression="zip",  # Archive old logs
    level="INFO",  # Default level
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
)

# You can configure more handlers here if needed
