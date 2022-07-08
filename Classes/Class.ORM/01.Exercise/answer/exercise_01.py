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
    title: str
    year: int

@datafile(data_filepattern)
class Actor(Model):
    id: int
    name: str
    birthday: str
    imdb: str
    movies: list[Movie]


if __name__ == '__main__':
    from movie_data import actors
    from pathlib import Path

    data_path = Path(data_dir)
    data_path.mkdir(exist_ok=True)

    for num, actor in enumerate(actors):
        d = dict(id=num)
        try:
            actor = d | actor
        except TypeError:
            actor = dict(d, **actor)
        act = Actor(**actor)
        print(act.id)
        act.datafile.save()
