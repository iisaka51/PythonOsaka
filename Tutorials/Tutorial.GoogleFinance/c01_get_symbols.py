from dataclasses import dataclass
import pandas as pd

@dataclass
class GFinance(object):
    name: str
    ticker: str

    def get_formula(self, attribute="price"):
        return f'=GoogleFinance("{self.ticker}", "{attribute}")'

def read_ticker(csv_file=None):
    companies = pd.read_csv(csv_file)
    companies['Price'] = [GFinance(c[1], c[2]).get_formula()
                             for c in companies.itertuples()]
    return companies

# df = read_ticker('GAFAM.csv')
