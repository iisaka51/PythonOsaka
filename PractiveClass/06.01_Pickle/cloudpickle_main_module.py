import pickle
import cloudpickle

CONSTANT = 42
def my_function(data: int) -> int:
    return data + CONSTANT

pickled_function = cloudpickle.dumps(my_function)
depickled_function = pickle.loads(pickled_function)
# depickled_function
# depickled_function(43)
