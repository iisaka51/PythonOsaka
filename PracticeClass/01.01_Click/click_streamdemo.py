#!/usr/bin/env python

import click
from click_stream import Stream
import bs4

url = "https://news.yahoo.co.jp/categories/it"
subsection="section.yjnSub_section div#accr .yjnSub_list_headline"
@click.command()
@click.option('--src', type=Stream(), default=url)
def cmd(src):
    soup = bs4.BeautifulSoup(src.read(), "lxml").text
    elements = soup.select(subsection)
    for e in elements:
        # 取得した見出しを表示
        print(">" + e.getText())

if __name__ == '__main__':
    cmd()
