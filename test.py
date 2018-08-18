import odbc
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup


def cleanStr(str):
    result = str.replace('\t', '')
    result = result.replace('\r', '')
    result = result.replace('\n', ' ')
    result = result.replace('+', '')
    result = result.replace('  ', '')
    result = result.split(' ')
    return result


id_title='Insurgency_Sandstorm'
id_num='581320'
type='app'

url = 'https://store.steampowered.com/' + str(type) + '/' + str(id_num) + '/' + str(id_title)
req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

ageCheck = soup.select(
    '#agecheck_form > h2'
)

contentWarning = soup.select(
    '#app_agegate > div > h2'
)

tags = soup.select(
    '#game_highlights > div > div > div > div > div.glance_tags.popular_tags'
)
# developers_list > a
developer = soup.select(
    '#developers_list > a'
)
# game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div > div:nth-child(5) > div.summary.column > a
publisher = soup.select(
    '#game_highlights > div > div > div > div > div > div.summary.column > a'
)
#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div > div:nth-child(1) > div.summary.column > span.game_review_summary
#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div > div:nth-child(1) > div.summary.column > span.game_review_summary.positive
recent_review = soup.select(
    '#game_highlights > div > div > div > div > div > div > span'
)

if(contentWarning or ageCheck):
    print('age check')
print(soup)
# if (ageCheck):
#     print("age check")
# else:
#     print(recent_review[0].text)
#     print(cleanStr(recent_review[1].text))
#     print((developer[0].text))
#     print(publisher[1].text)
#     print(cleanStr(tags[0].text))
