import math

def compute_roots(nums):
    result = []
    for n in nums:
        result.append(math.sqrt(n))
    return result

nums = range(10000)
for n in range(1000):
    r = compute_roots(nums)
