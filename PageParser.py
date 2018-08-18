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

####
connect = odbc.odbc('oasis')
db = connect.cursor()
db.execute("SELECT id_title, id_num, type FROM oasis.games LIMIT 100")
result = db.fetchall()

id_num = []
id_title = []
type = []

for i in result:
    id_title.append(i[0])
    id_num.append(i[1])
    type.append(i[2])

####


for i in range(50,100):

    url = 'https://store.steampowered.com/' + str(type[i]) + '/' + str(id_num[i]) + '/' + str(id_title[i])
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

    recent_review = soup.select(
        '#game_highlights > div > div > div > div > div > div > span'
    )

    if (ageCheck or contentWarning):
        print(id_title[i], "  ", i)
        print("age check")
        print("----------------------------------")
    else:
        print(id_title[i], "  ", i)
        if(recent_review):
            print(recent_review[0].text)
            print(cleanStr(recent_review[1].text))
        if(developer):
            print((developer[0].text))
        if(publisher):
            print(publisher[1].text)
        if(tags):
            print(cleanStr(tags[0].text))
        print("----------------------------------")
