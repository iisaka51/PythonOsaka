import logging

formatter = logging.Formatter(
    '%(levelname)s:%(asctime)s:%(lineno)d:%(name)s:%(message)s')

logger = logging.getLogger()
fh = logging.FileHandler('test.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
logger.debug('This is sample.')

# !cat test.log
