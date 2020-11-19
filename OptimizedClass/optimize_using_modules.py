import math
import numpy as np

def list_append(x):
    results = []
    for i in range(x):
        results.append(math.sqrt(i))
    return results

def list_comp(x):
    results = [math.sqrt(i) for i in range(x)]
    return results

def list_map(x):
    results = map(math.sqrt, range(x))
    return results

def list_numpy(x):
    results = list(np.sqrt(np.arange(x)))
    return results
