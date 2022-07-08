from __future__ import print_function
from behold import Behold, Item

class CustomBehold(Behold):
    @classmethod
    def load_state(cls):
        cls.name_lookup = {
            1: 'John',
            2: 'Paul',
            3: 'George',
            4: 'Ringo'
        }
        cls.instrument_lookup = {
            1: 'Rhythm Guitar',
            2: 'Bass Guitar',
            3: 'Lead Guitar',
            4: 'Drums'
        }

    def extract(self, item, name):
        """
        beholdクラスのextract()メソッドをオーバーライドしています
        このメソッドは、オブジェクトを受け取り、それを文字列に変換します
        デフォルトの動作は、オブジェクトに対して単にstr()を呼び出します
        """
        if not hasattr(self.__class__, 'name_lookup'):
            self.__class__.load_state()

        val = getattr(item, name)

        if isinstance(item, Item) and name == 'name':
            return self.__class__.name_lookup.get(val, None)

        elif isinstance(item, Item) and name == 'instrument':
            return self.__class__.instrument_lookup.get(val, None)

        # otherwise, just call the default extractor
        else:
            return super(CustomBehold, self).extract(item, name)


items = [Item(name=nn, instrument=nn) for nn in range(1, 5)]

print('\n# 標準のBeholdクラスを使ってアイテムを出力')
for item in items:
    _ = Behold().show(item)


print('\n# CustomBeholdクラスを使用したアイテムを専用エクストラクタで出力する')
for item in items:
    _ = CustomBehold().show(item, 'name', 'instrument')
