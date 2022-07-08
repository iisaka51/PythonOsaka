import logging

LOGGER = logging.getLogger(__name__)

def test_loglevel():
    LOGGER.info('lOGLevel info')
    LOGGER.warning('lOGLevel warning')
    LOGGER.error('lOGLevel error')
    LOGGER.critical('lOGLevel critical')
    assert True
