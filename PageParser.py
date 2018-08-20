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
    # if (result.isdigit()):
    #     return result
    # else:
    #     return 0
    return result


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
    # print(info)
    result = info.replace('\t', '').replace('\r', '').split('\n')
    while ('' in result):
        result.remove('')
    print(result)

    if ('Recent' in result[0]):

        idx = 1

        if (cleanNum(result[2]).isdigit() == False):
            print("False")
            idx = 0
            recent_review_num = 0
            recent_review = result[1]
        else:
            recent_review_num = cleanNum(result[idx + 1])
            recent_review = result[1]

        recent_review_percentage = '0%'
        a = result[idx + 2].split(' ')
        for col in a:
            if ('%' in col):
                recent_review_percentage = col

        all_review_percentage = '0%'
        a = result[idx + 6].split(' ')
        for col in a:
            if ('%' in col):
                all_review_percentage = col

        return {
            'recent_review': recent_review,
            'recent_review_num': recent_review_num,
            'recent_review_percentage': recent_review_percentage,
            'all_review': result[idx + 4],
            'all_review_num': cleanNum(result[idx + 5]),
            'all_review_percentage': all_review_percentage

        }
    else:
        if ('No' in result[1]):
            return {
                'recent_review': 'NONE',
                'recent_review_num': 0,
                'recent_review_percentage': '0%',
                'all_review': 'NONE',
                'all_review_num': 0,
                'all_review_percentage': '0%'
            }

        all_review_percentage = '0%'
        a = result[3].split(' ')
        for col in a:
            if ('%' in col):
                all_review_percentage = col

        return {
            'recent_review': 'NONE',
            'recent_review_num': 0,
            'recent_review_percentage': '0%',
            'all_review': result[1],
            'all_review_num': cleanNum(result[2]),
            'all_review_percentage': all_review_percentage
        }


####
connect = odbc.odbc('oasis')
db = connect.cursor()

db.execute("select id_title, id_num, type, max(title) from oasis.games group by id_title")
result = db.fetchall()

id_num = []
id_title = []
type = []

for i in result:
    id_title.append(i[0])
    id_num.append(i[1])
    type.append(i[2])

####


connect = odbc.odbc('oasis')
db = connect.cursor()
sql = '''
    INSERT INTO oasis.test_page(id_title, id_num, recent_review, recent_review_num, recent_review_percentage, all_review, all_review_num, all_review_percentage, tag) VALUES ("%s","%s","%s","%d","%s","%s","%d","%s","%s")
    '''

games = []
cnt = 0
total_cnt = 0
total_row = len(result)
pass_cnt = 0

for i in result:
    # if(pass_cnt<328):
    #     pass_cnt=pass_cnt+1
    #     continue
    # sleep(0.1)
    total_cnt = total_cnt + 1
    id_title = i[0]
    id_num = i[1]
    type = i[2]

    if (id_title == 'NONE'):
        continue
    game = {}
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

    info = soup.select(
        '#game_highlights > div > div > div.glance_ctn_responsive_left > div '
    )

    if (ageCheck or contentWarning):
        print(id_title)
        print("age check")
        print("--------------------END--------------------", '[', total_cnt, '/', total_row, ']', '----------------------------')
    else:
        cnt = cnt + 1
        print(id_title)
        a = getReviews(info[0].text)
        print(a)
        game['id_title'] = id_title
        game['id_num'] = id_num
        game['recent_review'] = a['recent_review']
        game['recent_review_num'] = a['recent_review_num']
        game['recent_review_percentage'] = a['recent_review_percentage']
        game['all_review'] = a['all_review']
        game['all_review_num'] = a['all_review_num']
        game['all_review_percentage'] = a['all_review_percentage']
        if (developer):
            print((developer[0].text))
            game['developer'] = developer[0].text
        else:
            game['developer'] = 'NONE'
        if (publisher and len(publisher) > 1):
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

        print("----------------SQL-INSERT-----------------", '----------------------------')
        print(game)
        try:
            db.execute(sql % (
                game['id_title'], game['id_num'], game['recent_review'], int(game['recent_review_num']),
                game['recent_review_percentage'],
                game['all_review'], int(game['all_review_num']), game['all_review_percentage'],
                game['tag']
            ))
        except ValueError:
            print("EXCEPTION OCCUR")
            pass

        print("--------------------END--------------------", '[', total_cnt, '/', total_row, ']', '----------------------------')
