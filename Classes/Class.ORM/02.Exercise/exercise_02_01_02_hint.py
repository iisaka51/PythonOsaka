import dataset
from pathlib import Path

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
    # ...
        print(f'   - "{movie["title"]}" {movie["year"]}')

db.commit()
db.executable.invalidate()
db.executable.engine.dispose()
db.close()
