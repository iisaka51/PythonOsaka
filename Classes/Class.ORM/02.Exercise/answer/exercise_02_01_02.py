import dataset
from sqlalchemy.types import Integer
from pathlib import Path
from movie_data import actors

data_dir = 'moviedb'
Path(data_dir).mkdir(exist_ok=True)

DSN = f'sqlite:///{data_dir}/movidb.sqlite'
db = dataset.connect(DSN)

actor_table = db['actor']
movie_table = db['movie']

actors = actor_table.all()
movies = movie_table.all()

for actor in actors:
    print(f'* Name: {actor["name"]}')
    print(f' - Birthday: {actor["birthday"]}')
    print(f' - IMDB: {actor["imdb"]}')
    print( ' - Movies: ')
    movie_ids = eval(actor['movies'])
    for movie_id in movie_ids:
        movie = movie_table.find_one(id = movie_id)
        print(f'   - "{movie["title"]}" {movie["year"]}')

db.commit()
db.executable.invalidate()
db.executable.engine.dispose()
db.close()
