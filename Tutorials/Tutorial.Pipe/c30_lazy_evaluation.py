from itertools import count
from pipe import select, where, take

def dummy_func(x):
    print(f"processing at value {x}")
    return x

print("----- test using a generator as input -----")

print(f"we are feeding in a: {type(count(100))}")

res_with_count = (count(100) | select(dummy_func)
                             | where(lambda x: x % 2 == 0)
                             | take(2))

print(f"the resulting object is: {res_with_count}")
print(f"when we force evaluation we get:")
print(f"{list(res_with_count)}")

print("----- test using a list as input -----")

list_to_100 = list(range(100))
print(f"we are feeding in a: {type(list_to_100)} which has length {len(list_to_100)}")

res_with_list = (list_to_100 | select(dummy_func)
                             | where(lambda x: x % 2 == 0)
                             | take(2))

print(f"the resulting object is: {res_with_list}")
print(f"when we force evaluation we get:")
print(f"{list(res_with_list)}")
