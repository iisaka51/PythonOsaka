import logging
import logging.config
from logconf import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger('demo')
log.debug('This is simple test')
