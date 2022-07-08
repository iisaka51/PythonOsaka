from pysimplelog import SingleLogger as LOG

class Logger(LOG):
    def custom_init(self, *args, **kwargs):
        # 必要に応じてここに何かコードを追加
        pass

attrs = [attr for attr in dir(Logger) if not attr.startswith('_')]

# help(Logger)
