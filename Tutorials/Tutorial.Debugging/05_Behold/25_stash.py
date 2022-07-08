from behold import Behold, get_stash

for nn in range(10):
    # stash()は、タグで作成されたビヨンドオブジェクトに対してのみ実行できます
    # タグはstashリストのグローバルキーになります
    behold = Behold(tag='my_stash_key')
    two_nn = 2 * nn

    _ = behold.stash('nn' 'two_nn')

# これをコードの全く別のファイルで実行します。
my_stashed_list = get_stash('my_stash_key')
