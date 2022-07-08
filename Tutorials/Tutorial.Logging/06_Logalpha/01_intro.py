from logalpha.contrib.standard import StandardLogger, StandardHandler

handler = StandardHandler()
StandardLogger.handlers.append(handler)

log = StandardLogger(__name__)

log.info('info message')
log.warning('waring message')
