import logging
import sys
from app.core.config import settings

def configure_logging():
    """
    Configure logging based on environment variables
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )
    
    # Set specific loggers to different levels if needed
    # For example, to reduce noise from third-party libraries:
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # In development, we might want more verbose SQL logging
    if settings.APP_ENVIRONMENT == "development":
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
