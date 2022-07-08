import logzero
from logzero import setup_logger

logger1 = setup_logger(name="mylogger1")
logger2 = setup_logger(name="mylogger2",
                       logfile="/tmp/test-logger2.log",
                       level=logzero.INFO)
logger3 = setup_logger(name="mylogger3",
                       logfile="/tmp/test-logger3.log",
                       level=logzero.INFO, disableStderrLogger=True)

# 何かをロギング
logger1.info("info for logger 1")
logger2.info("info for logger 2")

# ファイルのみにログを記録する(stderrへのログはしない)
logger3.info("info for logger 3")

# カスタムフォーマットにJSONフォーマットを使用
jsonLogger = setup_logger(name="jsonLogger", json=True)
jsonLogger.info("info in json")
