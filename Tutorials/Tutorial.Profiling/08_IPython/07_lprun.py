def sum_of_lists(N):
    total = 0
    for i in range(5):
        L = [j ^ (j >> i) for j in range(N)]
        total += sum(L)
    return total

# %load_ext line_profiler
# %lprun -f sum_of_lists sum_of_lists(5000)
