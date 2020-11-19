from loguru import logger

logger.add('/tmp/test.log', serialize=True)

logger.info("This is first log")
logger.info("This is second log")
