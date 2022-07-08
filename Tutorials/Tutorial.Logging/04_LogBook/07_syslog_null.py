from logbook import SyslogHandler, NullHandler
from bash import bash

error_handler = SyslogHandler('logbook example', level='ERROR')
null_handler = NullHandler()

with null_handler.applicationbound():
    with error_handler.applicationbound():
        # 何かの処理が実行されて
        # ERRORは error_handler に送られる
        # それ以外はすべてnull handlerに吸収されるため、
        # デフォルトの stderr ハンドラには何も送られない
        bash('ls /tmp/missing_file')
