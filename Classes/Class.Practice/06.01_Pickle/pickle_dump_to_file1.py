import pickle
import sys

class SimpleObject:
    def __init__(self, name, val):
        self.name = name
        l = list(name)
        l.reverse()
        self.name_backwards = ''.join(l)
        self.val = val

if __name__ == '__main__':
    data = []
    # data.append(SimpleObject('pickle'))
    # data.append(SimpleObject('preserve'))
    # data.append(SimpleObject('last'))
    data.append(SimpleObject('sample', 1.0))

    filename = sys.argv[1]

    with open(filename, 'wb') as out_s:
        for o in data:
            print(f'WRITING: {o.name} ({o.name_backwards})')
            pickle.dump(o, out_s)
