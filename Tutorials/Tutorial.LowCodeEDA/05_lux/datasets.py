import pandas as pd
from pathlib import Path
from urllib.error import HTTPError

class DatasetError(BaseException):
    pass

class DataSet(object):
    baseurl = 'https://raw.githubusercontent.com/adamerose/datasets/master/'
    dataset_names = [
        'anscombe.csv',
        'attention.csv',
        'brain_networks.csv',
        'country_indicators.csv',
        'diamonds.csv',
        'dots.csv',
        'exercise.csv',
        'flights.csv',
        'fmri.csv',
        'gammas.csv',
        'gapminder.csv',
        'geyser.csv',
        'googleplaystore.csv',
        'googleplaystore_reviews.csv',
        'happiness.csv',
        'harry_potter_characters.csv',
        'iris.csv',
        'mi_manufacturing.csv',
        'mpg.csv',
        'netflix_titles.csv',
        'penguins.csv',
        'planets.csv',
        'pokemon.csv',
        'reddit_showerthoughts_may2015.csv',
        'seinfeld_episodes.csv',
        'seinfeld_scripts.csv',
        'stockdata.csv',
        'tips.csv',
        'titanic.csv',
        'trump_tweets.csv',
        'us_shooting_incidents.csv',
    ]

    def load_dataset(self, name, save=False):
        try:
            assert name in self.dataset_names
            exists_flag = Path(name).exists()
            if exists_flag:
                url = 'file://' + str(Path(name).absolute())
            else:
                url = self.baseurl + name
            df = pd.read_csv( url )
            _ = save and not exists_flag and df.to_csv(name)
            return df
        except AssertionError:
            raise DatasetError('dataset not available') from None
        except HTTPError as err:
            raise DatasetError(err)

    def get_dataset_names(self):
        return self.dataset_names

dataset = DataSet()
load_dataset = dataset.load_dataset
get_dataset_names = dataset.get_dataset_names


if __name__ == '__main__':
    import sys
    if len(sys.argv)<=1:
        from pprint import pprint
        pprint(get_dataset_names())
    else:
        _= load_dataset(sys.argv[1], save=True)

