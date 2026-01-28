import sys
from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()


logger.add(sys.stdout, serialize=True, level="INFO")


logger.add(
    LOG_DIR / "app.log", rotation="1 week", retention="1 month", serialize=True, level="INFO"
)
