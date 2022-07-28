from scrapinghelper import Scraper

url = 'https://news.yahoo.co.jp'

scraper = Scraper()
response = scraper.request(url)

news_links = scraper.get_links(response.html, containing="pickup")
