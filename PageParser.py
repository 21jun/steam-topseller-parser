import odbc
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup

type = 'app'
id_num ='570'
id_title = 'Dota_2'
url = 'https://store.steampowered.com/'+str(type)+'/'+str(id_num)+'/'+str(id_title)
req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

def cleanStr(str):
    result = str.replace('\t', '')
    result = result.replace('\r', '')
    result = result.replace('\n', ' ')
    result = result.replace('+', '')
    return result



tags = soup.select(
    '#game_highlights > div > div > div > div > div.glance_tags.popular_tags'
)


print(cleanStr(tags[0].text))
