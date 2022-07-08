import logging
from pylogrus import PyLogrus, JsonFormatter

enabled_fields = [
    ('name', 'logger_name'),
    ('asctime', 'service_timestamp'),
    ('levelname', 'level'),
    ('threadName', 'thread_name'),
    'message',
    ('exception', 'exception_class'),
    ('stacktrace', 'stack_trace'),
    'module',
    ('funcName', 'function')
]

formatter = JsonFormatter(datefmt='Z',
                enabled_fields=enabled_fields, indent=2, sort_keys=True)

logging.setLoggerClass(PyLogrus)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug('This is simple test.')
