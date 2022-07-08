import requests

base_url = 'https://github.com/mihi-tr/Airport-Data'
url = base_url + '/raw/master/data/db/airports.sqlite'
response = requests.get(url)

with open('airports.sqlite', 'wb') as f:
        f.write(response.content)
