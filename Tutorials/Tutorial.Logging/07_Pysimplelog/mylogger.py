from pysimplelog import Logger

# 初期化
logger = Logger("log test")

# ログファイル名を設定
logger.set_log_file_basename("mylog")

# ログファイルの拡張子を設定
logger.set_log_file_extension("pylog")

# 新規のログタイプを追加
logger.add_log_type("super critical",
               name="SUPER CRITICAL", level=200, color='red',
               attributes=["bold","underline"])
logger.add_log_type("wrong",
               name="info", color='magenta',
               attributes=["strike through"])
logger.add_log_type("important",
               name="info", color='black', highlight="orange",
               attributes=["bold"])

# error ログタイプ を更新
logger.update_log_type(logType='error', color='pink',
                  attributes=['underline','bold'])

if __name__ == '__main__':
    print(logger)
