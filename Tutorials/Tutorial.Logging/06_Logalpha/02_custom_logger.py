from oklogger import *

handler = OkayHandler()
OkayLogger.handlers.append(handler)

log = OkayLogger()

log.ok('operation succeeded')
