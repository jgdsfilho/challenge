import logging

from app import Settings

settings = Settings()

log_level = logging.DEBUG if settings.debug else logging.INFO

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=log_level,
    handlers=[
        logging.StreamHandler(),
    ],
)
