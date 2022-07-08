from BTrees.OOBTree import OOSet

L1, L2, L3 = [1], [2], [3]
s = OOSet((L2, L3, L1))

v1 = list(s.keys())
v2 = s.has_key([3])
v3 = L2[0] = 5
v4 = s.has_key([3])

# print(s)
# print(v1)
# print(v2)
# print(v3)
# print(v4)
