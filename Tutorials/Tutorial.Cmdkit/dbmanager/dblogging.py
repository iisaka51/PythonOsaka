import sys
from cmdkit.app import log
import logging

log_stderr = logging.StreamHandler(sys.stderr)
log_stderr.setLevel(logging.WARNING)
log_stderr.setLevel(logging.CRITICAL)

log.addHandler(log_stderr)
