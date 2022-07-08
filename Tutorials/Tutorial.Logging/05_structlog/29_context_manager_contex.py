import structlog
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
    merge_contextvars,
    unbind_contextvars,
)

structlog.configure(
    processors=[
        merge_contextvars,
        structlog.processors.KeyValueRenderer(key_order=["event", "a"]),
    ]
)

log = structlog.get_logger()

clear_contextvars()
bind_contextvars(a=1, b=2)

# log.msg("hello")
# log.msg("world")

# clear_contextvars()
# log.msg("hi there")
