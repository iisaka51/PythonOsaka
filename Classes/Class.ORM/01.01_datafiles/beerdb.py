from dataclasses import dataclass
from datafiles import *

data_dir = './beerdb'
data_pattern = data_dir + '/{self.brewery}.yml'

@dataclass
class Beer:
    name: str
    abv: float   # Alcohol by Volume (アルコール度数)

@datafile(data_pattern)
class Drink:
    brewery: str
    data: Beer

if __name__ == '__main__':
    from pathlib import Path

    dir = Path(data_dir)
    dir.mkdir(exist_ok=True)

    beers =[
        {'brewery': 'Minoh', 'data': {'name': 'Pale_Ale', 'abv': 5.5} },
        {'brewery': 'Kyoto', 'data': {'name': 'ICHII_SENSHI', 'abv': 6.5} },
        {'brewery': 'Plank', 'data': {'name': 'Pilserl', 'abv': 4.9} },
    ]

    for beer in beers:
        v1 = Drink(**beer)

