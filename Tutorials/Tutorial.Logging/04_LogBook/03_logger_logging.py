import sys
import logging

ch = logging.StreamHandler(sys.stderr)
logger = logging.getLogger('logging demo')
logger.addHandler(ch)
logger.warning('Hello Python')
