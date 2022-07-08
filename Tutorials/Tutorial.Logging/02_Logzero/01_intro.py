from logzero import logger

logger.debug("hello")
logger.info("info")
logger.warning("warn")
logger.error("error")

try:
    raise Exception("this is a demo exception")
except Exception as e:
    logger.exception(e)

# logger.info("test")
