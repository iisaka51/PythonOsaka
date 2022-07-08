import logzero
from logzero import logger

# non-rotating logfile
logzero.logfile("/tmp/logfile.log")

# rotating logfile
logzero.logfile("/tmp/rotating-logfile.log",
                maxBytes=1e6, backupCount=3)

# log messages
logger.info("This message output to the console and the logfile")
