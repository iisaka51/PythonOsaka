import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug('This is simple test')
