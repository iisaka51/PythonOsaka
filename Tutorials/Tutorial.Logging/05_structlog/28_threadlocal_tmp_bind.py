import structlog
from structlog.threadlocal import tmp_bind

log = structlog.get_logger()

log.bind(x=42)
log.msg("event!")

with tmp_bind(log, x=23, y="foo") as tmp_log:
    tmp_log.msg("another event!")

log.msg("one last event!")
