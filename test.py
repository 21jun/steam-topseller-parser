import odbc
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/stats/Steam-Game-and-Player-Statistics'
req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

total_players = soup.select(
    'body > div > div > div > div > div.page_content > div > div > div > div > table > tr'
)


def aaa():
    a = ["f", "s","fs"]
    return a


aa, bb, cc = aaa()
print(aa,bb,cc)