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


def cleanNum(str):
    result = str.replace('(', '')
    result = result.replace(')', '')
    result = result.replace(',', '')
    if(result.isdigit()):
        return result
    else:
        return 0


def getTags(tags):
    result = tags.replace('\t', '')
    result = result.replace('\r', '')
    result = result.replace('\n', ' ')
    result = result.replace('+', '')
    result = result.replace('  ', '')
    result = result.split(' ')
    result.remove('')
    return result


def getReviews(info):
    r1 = info[0].text.replace('\t', '').replace('\r', '').split('\n')
    while ('' in r1):
        r1.remove('')

    r2 = info[1].text.replace('\t', '').replace('\r', '').split('\n')
    while ('' in r2):
        r2.remove('')

    if ('Recent' in r1[0]):  # recent 리뷰가 있으면 all 리뷰도 존재(r2)
        return {
            'recent_review': r1[1],
            'recent_review_num': cleanNum(r1[2]),
            'all_review': r2[1],
            'all_review_num': cleanNum(r2[2])
        }

    else:  # recent 리뷰가 없으면 all 리뷰가 r1
        if ('No' in r1[1]):
            return {
                'recent_review': 'NONE',
                'recent_review_num': 0,
                'all_review': 'NONE',
                'all_review_num': 0
            }
        return {
            'recent_review': 'NONE',
            'recent_review_num': 0,
            'all_review': r1[1],
            'all_review_num': cleanNum(r1[2])
        }


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

games = []

for i in range(0, 10):

    game = {}
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

    info = soup.select(
        '#game_highlights > div > div > div > div > div'
    )

    if (ageCheck or contentWarning):
        print(id_title[i], "  ", i)
        print("age check")
        print("----------------------------------")
    else:
        print(id_title[i], "  ", i)
        a = getReviews(info)
        print(a)
        game['id_title'] = id_title[i]
        game['id_num']= id_num[i]
        game['recent_review'] = a['recent_review']
        game['recent_review_num'] = a['recent_review_num']
        game['all_review'] = a['all_review']
        game['all_review_num'] = a['all_review_num']
        if (developer):
            print((developer[0].text))
            game['developer'] = developer[0].text
        else:
            game['developer'] = 'NONE'
        if (publisher):
            print(publisher[1].text)
            game['publisher'] = publisher[1].text
        else:
            game['publisher'] = 'NONE'
        if (tags):
            print(getTags(tags[0].text))
            _tags = ','.join(getTags(tags[0].text))
            game['tag'] = _tags
        else:
            game['tag'] = 'NONE'
        print("----------------------------------")

        games.append(game)

for i in games:
    print(i)

connect = odbc.odbc('oasis')
db = connect.cursor()
sql = '''
    INSERT INTO oasis.test_page(id_title, id_num, recent_review, recent_review_num, all_review, all_review_num, tag) VALUES ("%s","%s","%s","%d","%s","%d","%s")
    '''
for i in games:
    db.execute(sql % (
        i['id_title'], i['id_num'], i['recent_review'], int(i['recent_review_num']), i['all_review'], int(i['all_review_num']),
        i['tag']
    ))

