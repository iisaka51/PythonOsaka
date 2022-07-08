from behold import Behold, Item

items = [
   Item(a=1, b=2),
   Item(c=3, d=4),
]

for item in items:
   # 内部表現の文字列をフィルター
   _ = Behold(tag='first').when_values(a='1').show(item)

   # Behold is smart enough to transform your criteria to strings
   # so this also works
   # Beholdは、criteriaを文字列に変換するので、次の表記もOK
   _ = Behold(tag='second').when_values(a=1).show(item)

   # operations.
   # 変数の内部表現の文字列はローカルスコープには存在しないので、
   # 論理演算には when_context() と同様な構文を使う必要があります。
   _ = Behold(tag='third').when_values(a__gte=1).show(item)
