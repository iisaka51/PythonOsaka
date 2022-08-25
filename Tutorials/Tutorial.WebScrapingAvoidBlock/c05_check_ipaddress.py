from scrapinghelper import Scraper, ProxyRotate

# using tor networks as tiny socks5 proxy
proxies = [ 'socks5://127.0.0.1:9050' ]
url = 'https://httpbin.org/ip'

scraper = Scraper(proxies=proxies)

response = scraper.request(url)
print(response.html.text)

# using next proxy server from pool
response = scraper.request(url,proxy_rotate=ProxyRotate.NEXT)
print(response.html.text)

# using current proxy server and does not call render()
response = scraper.request(url,proxy_rotate=ProxyRotate.KEEP, render=False)
print(response.html.text)
