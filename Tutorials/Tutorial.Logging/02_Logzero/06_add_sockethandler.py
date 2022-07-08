import logzero
import logging
from logging.handlers import SocketHandler, DEFAULT_TCP_LOGGING_PORT

# SocketHandler の設定
socket_handler = SocketHandler('localhost', DEFAULT_TCP_LOGGING_PORT)
socket_handler.setLevel(logzero.DEBUG)
socket_handler.setFormatter(logzero.LogFormatter(color=False))

# logzero のデフォルトロガーに追加
logzero.logger.addHandler(socket_handler)

logzero.logger.info("this is a test")
