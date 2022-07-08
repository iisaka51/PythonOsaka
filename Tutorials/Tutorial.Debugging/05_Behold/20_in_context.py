from behold import BB  # this is an alias for Behold
from behold import in_context

def my_function():
    for nn in range(5):
        x, y = nn, 2 * nn

        # 'testing' の時だけ出力
        BB().when_context(what='testing').show('x')

        # 'production' の時だけ出力
        BB().when_context(what='production').show('y')

# デコレーターを使った'testing' 用コンテキストの設定
@in_context(what='testing')
def test_x():
   my_function()

# テストを実行
test_x()

# コンテキストマネージャを使用して'production'用のコンテキストを設定し
with in_context(what='production'):
   my_function()
