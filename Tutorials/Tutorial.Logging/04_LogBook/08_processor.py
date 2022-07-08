import os
from logbook import Processor

def inject_cwd(record):
    record.extra['cwd'] = os.getcwd()

with my_handler.applicationbound():
    with Processor(inject_cwd).applicationbound():
        # ここでロギングされたものは、
        # ログレコードにカレントワーキングディレクトリが表示されます。
        pass
