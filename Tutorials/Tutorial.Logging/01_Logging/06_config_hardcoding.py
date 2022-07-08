import logging

formatter = logging.Formatter(
     '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug('This is simple test')
