def sum_of_lists(N):
    total = 0
    for i in range(5):
        L = [j ^ (j >> i) for j in range(N)]
        total += sum(L)
    return total

# %load_ext memory_profiler
# %memit sum_of_lists(1000000)
