import logging
logging.basicConfig()

from structlog.stdlib import LoggerFactory
structlog.configure(logger_factory=LoggerFactory())
log = structlog.get_logger()
log.warning("it works!", difficulty="easy")
