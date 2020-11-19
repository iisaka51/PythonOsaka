from logging import getLogger, StreamHandler
import sys

StreamHandler(sys.stdout).push_application()
mylog = getLogger('My Log')

from logbook.compat import RedirectLoggingHandler
mylog.addHandler(RedirectLoggingHandler())
otherlog = getLogger('Other Log')
otherlog.warn('logging is deprecated')
mylog.warning('but logbook is awesome')
