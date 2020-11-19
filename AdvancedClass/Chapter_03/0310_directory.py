import os
dirpath = os.path.abspath(os.path.dirname(__file__))
scriptpath = os.path.join(dirpath, __file__)
cwd = os.getcwd()
print(f'Current Working Directory: {cwd}')
print(f'Directory path: {dirpath}')
print(f'Script path: {scriptpath}')
