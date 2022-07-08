from pprint import pprint
from behold import Behold, in_context, get_stash, clear_stash

def my_function():
    out = []
    for nn in range(5):
        x, y, z = nn, 2 * nn, 3 * nn
        out.append((x, y, z))

        # 変数を隠しておきたい場合は、タグを定義しておく必要があります
        # タグの名前は、グローバルスタッシュスペースのキーとなります
        # 次は'test_x'の時にのみ出力されます
        Behold(tag='test_x').when_context(what='test_x').stash('y', 'z')

        # 次は'test_y'のテスト時にのみ出力されます
        Behold(tag='test_y').when_context(what='test_y').stash('x', 'z')

        # 次は'test_z'のテスト時にのみ出力されます
        Behold(tag='test_z').when_context(what='test_z').stash('x', 'y')
    return out


@in_context(what='test_x')
def test_x():
    assert(sum([t[0] for t in my_function()]) == 10)

@in_context(what='test_y')
def test_y():
    assert(sum([t[1] for t in my_function()]) == 20)

@in_context(what='test_z')
def test_z():
    assert(sum([t[2] for t in my_function()]) == 30)

test_x()
test_y()
test_z()


print('\n# test_x のスタッシュの結果。y と z の値だけを期待している')
pprint(get_stash('test_x'))

print('\n# test_y のスタッシュの結果。x と z の値だけを期待している')
pprint(get_stash('test_y'))

print('\n# test_z のスタッシュの結果。x と y の値だけを期待している')
pprint(get_stash('test_z'))

# 引数がない場合、clear_stash() はすべてのスタッシュを削除されます
# 名前を指定することで、消去する特定のスタッシュを選択できます
clear_stash()
