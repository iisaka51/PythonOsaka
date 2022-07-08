import logging
import logzero
from logzero import logger
from logging.handlers import SysLogHandler

# コンソールへログメッセージを出力
logger.debug("hello")

# 最小のログレベルに設定
logzero.loglevel(logzero.INFO)

# ログファイルを設定(以後のログはこのファイルに書き込まれる)
logzero.logfile("/tmp/logfile.log")

# ログファイルを設定(以後のログはこのファイルに書き込まれる)
# デフォルトの標準エラー出力はしなくなる
logzero.logfile("/tmp/logfile.log", disableStderrLogger=True)

# ログ・ファイルごとに異なるログレベルを設定することができる
logzero.logfile("/tmp/logfile.log", loglevel=logzero.ERROR)

# ログファイルにローテーションを設定
logzero.logfile("/tmp/rotating-logfile.log", maxBytes=1000000, backupCount=3)

# ファイルへのログ出力を無効に設定
logzero.logfile(None)

# JSONフォーマットを有効に設定
logzero.json()

# JSONフォーマットを無効に設定
logzero.json(False)

# logzero のデフォルトの出力先を syslog に設定 syslog facility は 'user'
logzero.syslog()

# logzero のデフォルトの出力先を syslog に設定 syslog facility は 'local0'
logzero.syslog(facility=SysLogHandler.LOG_LOCAL0)

# カスタムフォーマットを設定
formatter = logging.Formatter(
    '%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
logzero.formatter(formatter)

# 指定したメッセージをログに出力 (この場合、ログレベルはINFO)
logger.info("var1: %s, var2: %s", 1, 'Python')
