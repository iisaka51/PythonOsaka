from behold import in_context
from myfunc import my_function

# コンテキスト 'testing' でデコレート
@in_context(what='testing')
def test_x():
    my_function()
test_x()

# 'debugging' をセットしたコンテキストマネージャ
with in_context(what='debugging'):
    my_function()
