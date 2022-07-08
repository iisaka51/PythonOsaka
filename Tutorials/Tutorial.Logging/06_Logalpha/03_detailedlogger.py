from detailedlogger import *
from logalpha.contrib.standard import StandardHandler

handler = StandardHandler()
DetailedLogger.handlers.append(handler)
log = DetailedLogger('custom log')

log.warning('runtime errors')
