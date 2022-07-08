from mylogger import logger

# 直近にログされたメッセージを出力
print("")
print("Last logged messages are:")
print("=========================")
print(logger.lastLoggedMessage)
print(logger.lastLoggedDebug)
print(logger.lastLoggedInfo)
print(logger.lastLoggedWarning)
print(logger.lastLoggedError)
print(logger.lastLoggedCritical)
