import parsl
from parsl.app.app import python_app
from parsl.data_provider.files import File

parsl.load()

@python_app
def sort_numbers(inputs=[]):
    with open(inputs[0].filepath, 'r') as f:
        strs = [n.strip() for n in f.readlines()]
        strs.sort()
        return strs

unsorted_file = File('https://raw.githubusercontent.com/Parsl/parsl-tutorial/master/input/unsorted.txt')

f = sort_numbers(inputs=[unsorted_file])
print (f.result())
