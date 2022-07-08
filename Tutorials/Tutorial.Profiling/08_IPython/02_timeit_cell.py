# %%timeit
total = 0
for i in range(1000):
    for j in range(1000):
        total += i * (-1) ** j
