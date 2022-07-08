x = {'a':1, 'b':2}
y = {'c':3, 'd':4}

z = x.copy()       # z=dict() ; z.update(x) と同じ
z.update(y)
print(z)
