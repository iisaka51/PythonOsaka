import structlog

cf = structlog.testing.CapturingLoggerFactory()
structlog.configure(logger_factory=cf,
                    processors=[structlog.processors.JSONRenderer()])
log = structlog.get_logger()

# log.info("test!")
# cf.logger.calls
