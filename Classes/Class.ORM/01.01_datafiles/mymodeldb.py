from datafiles import *

data_dir = './mymodels'
data_pattern = data_dir + '/{self.my_key}.yml'

@datafile(data_pattern)
class MyModel:
     my_key: str
     my_value: int = 0

if __name__ == '__main__':
    from pathlib import Path

    dir = Path(data_dir)
    dir.mkdir(exist_ok=True)
