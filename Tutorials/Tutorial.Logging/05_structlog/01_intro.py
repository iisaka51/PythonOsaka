import structlog

log = structlog.get_logger()
log.msg("greeted", whom="world", more_than_a_string=[1, 2, 3])
