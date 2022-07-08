v1 = select((p, count(p.cars)) for p in Person)[:]

# print(v1)
