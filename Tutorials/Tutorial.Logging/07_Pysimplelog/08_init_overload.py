from pysimplelog import SingleLogger as LOG

class Logger(LOG):
    def __init__(self, *args, **kwargs):
        if self._isInitialized: return
        super(Logger, self).__init__(*args, **kwargs)
        # 必要に応じてここに何かコードを追加
