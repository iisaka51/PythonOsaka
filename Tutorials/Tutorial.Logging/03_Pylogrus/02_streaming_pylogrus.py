import logging
from pylogrus import PyLogrus, TextFormatter           # 追加

formatter = TextFormatter(datefmt='Z', colorize=True)  # 修正

logging.setLoggerClass(PyLogrus)                       # 追加
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug('This is simple test.')
