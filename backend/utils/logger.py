from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format="{time} | {level} | {message}",
    level="INFO",
)

logger.add(
    "backend/logs/app.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
)

app_logger = logger