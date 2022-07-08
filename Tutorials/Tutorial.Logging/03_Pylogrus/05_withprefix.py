import logging
from pylogrus import PyLogrus, TextFormatter

formatter = TextFormatter(datefmt='Z', colorize=True)

logging.setLoggerClass(PyLogrus)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger = logger.withPrefix("[DEMO]")
logger.debug('This is simple test.')
