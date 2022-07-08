import logging

formatter = logging.Formatter(
    '%(asctime)s:%(lineno)d:%(name)s:%(levelname)s:%(message)s')

logger = logging.getLogger(__name__)
handler = logging.FileHandler('sample.log')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug('This is simple test')

# !cat sample.log
