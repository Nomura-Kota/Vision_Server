from src.vision_server.configs.config import config
from src.vision_server.loggers.logger import logger

DOUBLE_LINE = "=" * 30

def print_config_content() -> None:
    logger.info(DOUBLE_LINE)
    logger.info("VISION_SERVER STARTUP")
    logger.info(DOUBLE_LINE)
    logger.info(f"LOG_LEVEL   : {config.LOG_LEVEL}")
    logger.info(f"VISION_MODEL: {config.VISION_MODEL}")
    logger.info(DOUBLE_LINE)
