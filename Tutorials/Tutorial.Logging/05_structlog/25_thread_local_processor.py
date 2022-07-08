import structlog
from structlog.threadlocal import (
    bind_threadlocal,
    clear_threadlocal,
    merge_threadlocal,
)

from structlog import configure

configure(
    processors=[
        merge_threadlocal,
        structlog.processors.KeyValueRenderer(),
    ]
)

log = structlog.get_logger()

clear_threadlocal()
bind_threadlocal(a=1)

# log.msg("hi")

# clear_threadlocal()
# log.msg("hi there")
