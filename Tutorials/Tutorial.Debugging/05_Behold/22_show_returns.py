from behold import Behold, Item
a, b = 1, 2
my_list = [a, b]

# ローカル変数の引数を出力
Behold().show('a', 'b')

# ローカル変数をキーワード引数で指定して出力
Behold().show(a=my_list[0], b=my_list[1])

# キーワード引数を使ってローカルス変数の値を出力しますが
# 指定された順序で出力されるようにする
Behold().show('b', 'a', a=my_list[0], b=my_list[1])

# オブジェクトの属性値を出力
item = Item(a=1, b=2)
Behold().show(item, 'a', 'b')

# show() の戻り値を使って、より多くのデバッグを制御する
a = 1
if Behold().when(a > 1).show('a'):
    import pdb; pdb.set_trace()
