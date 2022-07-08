from behold import Behold

def my_function():
    x = 'hello'  # 何かしらの処理

    # コンテキストが 'testing' のときだけ x の値を出力
    Behold().when_context(what='testing').show('x')

    # コンテキストが 'debugging' のときだけ、デバッガを起動
    if Behold().when_context(what='debugging').is_true():
        import pdb; pdb.set_trace()

