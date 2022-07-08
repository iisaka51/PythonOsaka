from blitzdb import Document, FileBackend

data_dir = './beerdb'
backend = FileBackend( data_dir )

class Beer(Document):
    pass

class Brewery(Document):
    pass


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
    import subprocess

    subprocess.call(['rm', '-rf', data_dir])
    population_database()
