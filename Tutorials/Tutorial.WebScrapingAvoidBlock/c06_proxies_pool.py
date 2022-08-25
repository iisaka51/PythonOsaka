from pathlib import Path
from scrapinghelper import Scraper, URL, ProxyManager

url = 'https://httpbin.org/ip'

scraper = Scraper()
this_directory = Path(__file__).parent
proxy_file = (this_directory / "tor_network.txt")
pm = ProxyManager(f'file://{str(proxy_file)}')

response = scraper.request(url)
print(response.html.text)

for _ in range(5):
    proxies = pm.next_proxy()
    print(proxies)
    #response = scraper.request(url,proxies=proxies, render=False)
    #print(response.html.text)
