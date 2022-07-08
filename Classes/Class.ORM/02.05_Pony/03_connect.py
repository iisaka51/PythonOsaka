from pathlib import Path

dir = Path.cwd()
dbfile = str(dir / 'database.sqlite')
db.bind(provider='sqlite', filename=dbfile, create_db=True)
