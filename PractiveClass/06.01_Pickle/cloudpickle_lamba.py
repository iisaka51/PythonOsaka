import pickle
import cloudpickle

squared = lambda x: x ** 2
pickled_lambda = cloudpickle.dumps(squared)

new_squared = pickle.loads(pickled_lambda)
val = new_squared(2)
print(val)
