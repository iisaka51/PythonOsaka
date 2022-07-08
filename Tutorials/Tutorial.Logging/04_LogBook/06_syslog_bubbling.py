from logbook import SyslogHandler
from bash import bash

error_handler = SyslogHandler('logbook example',
                              level='ERROR', bubble=True)
with error_handler.applicationbound():
    # 何かの処理が実行されて
    # ERROR は error_handler へロギングされる
    bash('ls /tmp/missing_file')
