from logbook import warn, StreamHandler
from logbook.compat import redirect_logging

redirect_logging()
StreamHandler(sys.stdout).push_application()
redirect_logging()

from logging import getLogger

log = getLogger('My Logger')
log.warning('This is a warning')
