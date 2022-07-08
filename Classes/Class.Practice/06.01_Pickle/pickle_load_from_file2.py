import sys
import pprint
import pickle
from pickle_dump_to_file1 import SimpleObject

filename = sys.argv[1]

with open(filename, 'rb') as in_s:
    while True:
        try:
            o = pickle.load(in_s)
        except EOFError:
            break
        else:
            print(f'READ: {o.name} ({o.name_backwards})')
