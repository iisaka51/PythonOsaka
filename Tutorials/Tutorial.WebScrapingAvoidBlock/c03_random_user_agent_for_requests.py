import random
import requests
from pprint import pprint

url = 'http://httpbin.org/headers'
user_agent_list = [
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; WOW64; Trident/5.0; BOIE9;ENUS)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; WOW64; Trident/5.0; BOIE9;ENUS)',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; Sony Xperia Tablet Z - 4.2.2 - API 17 - 1920x1200 Build/JDQ39E) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900P Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en',
    'Host': 'httpbin.org',
    'Upgrade-Insecure-Requests': '1',
}

for n in range(1, 5):
    user_agent = random.choice(user_agent_list)
    headers['User-Agent'] = user_agent
    response = requests.get(url, headers=headers)
    print(f'Request: #{n}')
    pprint(response.json())
