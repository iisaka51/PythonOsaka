from BTrees.OOBTree import OOBTree

t = OOBTree()
t.update({1: "heart", 2: "diamond", 3: "spade", 4: "club"})
s = t.keys()

v1 = len(t)
v2 = t[2]
v3 = len(s)
v4 = s[-2]
v5 = list(s)
v6 = list(t.values())
v7 = list(t.values(1, 2))
v8 = list(t.values(2))

# print(v1)
# print(v2)
# print(v3)
# print(v4)
# print(v5)
# print(v6)
# print(v7)
# print(v8)
