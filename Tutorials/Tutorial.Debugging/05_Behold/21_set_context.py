from behold import Behold
from behold import set_context, unset_context

set_context(what='my_context')

# コンテキストの変数を出力
_ = Behold().when_context(what='my_context').show(x='hello')

unset_context('what')
