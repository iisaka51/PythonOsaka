@python_app
def pi(num_points):
    from random import random

    inside = 0
    for i in range(num_points):
        x,, y = random(), random()
        if x**2 + y**2 < 1:
            inside += 1

    return (inside*4 / num_points)

pi_future = pi(10**7)
print(pi_futures.result())
