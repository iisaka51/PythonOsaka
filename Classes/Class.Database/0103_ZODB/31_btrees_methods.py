from BTrees.OOBTree import OOBTree

t = OOBTree()
t.update({1: "red", 2: "green", 3: "blue", 4: "spades"})

v1 = list(t.values(min=1, max=4))
v2 = list(t.values(min=1, max=4, excludemin=True, excludemax=True))
v3 = t.minKey()
v4 = t.minKey(1.5)
v5 = t.has_key(4)
v6 = t.has_key(5)
v7 = 4 in t
v8 = 5 in t

# print(v1)
# print(v2)
# print(v3)
# print(v4)
# print(v5, v6)
# print(v7, v8)
