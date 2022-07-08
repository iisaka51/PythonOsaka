from datafiles import *
from dataclasses import dataclass
from datetime import datetime

"""
This script for Python 3.9
Ther's more than one way to do it.
    -- Larry Wall
"""

data_dir = 'moviedb'
data_filepattern = data_dir + '/{self.id}.json'

@dataclass
class Movie(Model):
    pass

@datafile(data_filepattern)
class Actor(Model):
    pass

if __name__ == '__main__':
    from pathlib import Path
    from movie_data import actors

    data_path = Path(data_dir)
    data_path.mkdir(exist_ok=True)

    for num, actor in enumerate(actors):
        d = dict(id=num)
        try:
            actor = d | actor      # python 3.9
        except:
            actor = dict(d, **actor)
        # この行以降を修正する必要がある
        print(actor)
