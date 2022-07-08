from structlog import get_logger
from structlog.testing import capture_logs

with capture_logs() as cap_logs:
   get_logger().bind(x="y").info("hello")

# cap_logs
