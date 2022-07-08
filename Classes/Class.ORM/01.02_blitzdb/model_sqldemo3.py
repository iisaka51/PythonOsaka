from sqlalchemy import create_engine
from pathlib import Path
from blitzdb import Document, SqlBackend
from blitzdb.fields import ( ForeignKeyField,
                             ManyToManyField,
                             CharField,
                             FloatField,
                             IntegerField,
                             BooleanField )

class Brewery(Document):
    name = CharField()
    country = CharField()
    product = ManyToManyField(related='Beer')

class Beer(Document):
    name = CharField()
    abv = FloatField()
    stock = IntegerField()
    brewery = ManyToManyField(related='Brewery')

data_dir = 'sqldemo'
dir = Path(data_dir)
dir.mkdir(exist_ok=True)

url = f'sqlite:///{data_dir}/demo.sqlite'
engine = create_engine(url, echo=False)
backend = SqlBackend(engine, ondelete='CASCADE')
backend.register(Beer)
backend.register(Brewery)
backend.init_schema()
backend.create_schema()

def population_database():
    # Alcohol by Volume (アルコール度数)
    beer_data = [
        { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
        { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
        { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
        { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ]

    brewery_data = [
        { 'name': 'Minoh', 'country': 'Japan' },
        { 'name': 'Kyoto', 'country': 'Japan' },
        { 'name': 'Plank', 'country': 'Germany' },
    ]

    for d in beer_data:
        v = Beer(d)
        v.save(backend)

    for d in brewery_data:
        v = Brewery(d)
        v.save(backend)

    backend.commit()

if __name__ == '__main__':
    population_database()
