import sys
from logbook import Logger, StreamHandler

StreamHandler(sys.stderr).push_application()
log = Logger('logbook demo')
log.warning('Hello Python')
