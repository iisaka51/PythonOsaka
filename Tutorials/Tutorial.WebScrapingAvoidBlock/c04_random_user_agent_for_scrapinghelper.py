import scrapinghelper as sch
from pprint import pprint

url = 'http://httpbin.org/headers'

scraper = sch.Scraper()

for n in range(1, 5):
    response = scraper.request(url, user_agent='random')
    print(f'Request: #{n}')
    pprint(response.json())
