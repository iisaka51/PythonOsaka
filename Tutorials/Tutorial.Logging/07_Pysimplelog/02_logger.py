from pysimplelog import Logger

logger = Logger()
print(logger)

attrs = [attr for attr in dir(logger) if not attr.startswith('_')]
