import logging

logger = logging.getLogger()
handler = logging.FileHandler('sample.log')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug('This is simple test')

# !cat sample.log
