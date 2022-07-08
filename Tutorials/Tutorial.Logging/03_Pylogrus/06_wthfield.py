import logging
from pylogrus import PyLogrus, TextFormatter

formatter = TextFormatter(datefmt='Z', colorize=True)
err_code = dict(error_code=404)

logging.setLoggerClass(PyLogrus)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger = logger.withFields(err_code)
logger.debug('This is simple test.')
