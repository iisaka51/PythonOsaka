import requests
from pprint import pprint

response = requests.get('http://httpbin.org/headers')
pprint(response.json())
