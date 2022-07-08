import os

cwd = os.getcwd()
for i in range(3):
    with open(os.path.join(cwd, f'hello-{i}.txt'), 'w') as f:
        c = f.write('hello {}\n'.format(i))
