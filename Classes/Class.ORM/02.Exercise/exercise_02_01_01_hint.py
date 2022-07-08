import dataset
from sqlalchemy.types import Integer
from sqlalchemy_utils import ScalarListType
from pathlib import Path
from movie_data import actors

data_dir = 'moviedb'
Path(data_dir).mkdir(exist_ok=True)

DSN = f'sqlite:///{data_dir}/movidb.sqlite'
db = dataset.connect(DSN)

actor_table = db['actor']
actor_table.create_column('id', type=Integer, autoincrement=True)
actor_table.create_index(['id'])

movie_table = db['movie']
movie_table.create_column('id', type=Integer, autoincrement=True)
movie_table.create_index(['id'])

movie_id = 0
for num, actor in enumerate(actors):
    movie_list = list()
    for movie in actor['movies']:
        # ...

    actor['movies'] = f'{movie_list}'
    actor_table.insert(actor)

db.commit()
db.executable.invalidate()
db.executable.engine.dispose()
db.close()
