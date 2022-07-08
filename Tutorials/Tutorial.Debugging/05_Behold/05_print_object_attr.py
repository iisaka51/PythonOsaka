from behold import Behold, Item

item = Item(a=1, b=2, c=3)

_ = Behold(tag='with_args').show(item, 'a', 'b')
_ = Behold(tag='no_args').show(item)
