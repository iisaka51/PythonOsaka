#import chardet
import requests
import bs4
from prettytable import from_html_one


with open('CITY.html') as fp:
    data = fp.read()

table = from_html_one(data)
print(table)
