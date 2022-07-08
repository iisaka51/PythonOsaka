from mylogger import logger

logger.info("I am info, called using my shortcut method.")
logger.log("info", "I am  info, called using log method.")

logger.warn("I am warn, called using my shortcut method.")
logger.log("warn", "I am warn, called using log method.")

logger.error("I am error, called using my shortcut method.")
logger.log("error", "I am error, called using log method.")

logger.critical("I am critical, called using my shortcut method.")
logger.log("critical", "I am critical, called using log method.")

logger.debug("I am debug, called using my shortcut method.")
logger.log("debug", "I am debug, called using log method.")

logger.log("super critical",
           "I am super critical, called using log method "
           "because I have no shortcut method.")
logger.log("wrong",
           "I am wrong, called using log method "
           "because I have no shortcut method.")
logger.log("important",
           "I am important, called using log method "
           "because I have no shortcut method.")
