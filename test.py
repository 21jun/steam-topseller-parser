import odbc
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup


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
def getTags(tags):
    try:
        result = tags.replace('\t', '')
        result = result.replace('\r', '')
        result = result.replace('\n', ' ')
        result = result.replace('+', '')
        result = result.replace('  ', '')
        result = result.split(' ')
        result.remove('')
    except:
        print("EXCEPT")
    return result


def cleanStr(str):
    result = str.replace('\t', '')
    result = result.replace('\r', '')
    result = result.replace('\n', ' ')
    # result = result.replace('  ', '')
    # result = result.replace(' ','')
    # result = result.split(' ')
    return result


def cleanNum(str):
    result = str.replace('(', '')
    result = result.replace(')', '')
    result = result.replace(',', '')
    return result


id_title = ''
id_num = '740080'
type = 'app'
# {'id_title': 'They_Are_Billions', 'id_num': '644930', 'recent_review': 'Mostly Positive', 'recent_review_num': 0, 'recent_review_percentage': '78%', 'all_review': 'No user reviews', 'all_review_num': 'Release Date:', 'all_review_percentage': '0%', 'developer': 'Numantian Games', 'publisher': 'Numantian Games', 'tag': 'Early,Access,Base,Building,Strategy,Survival,Zombies,RTS,Steampunk,Post-apocalyptic,City,Builder,Building,Tower,Defense,Singleplayer,Resource,Management,Real-Time,with,Pause,Early,Access,Tactical,Difficult,Management,Indie,Isometric'}
url = 'https://store.steampowered.com/' + str(type) + '/' + str(id_num) + '/' + str(id_title)
req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')


#print(soup)

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

publisher = soup.select(
    '#game_highlights > div > div > div > div > div > div.summary.column > a'
)

recent_review = soup.select(
    '#game_highlights > div > div > div > div > div > div > span'
)

# game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div

info = soup.select(
    '#game_highlights > div > div > div.glance_ctn_responsive_left > div '
)

try:
    information = info[0]
except IndexError:
    print("INDEX OUT OF RANGE")
    quit()
# print(information)
a = getReviews(information.text)
#print(a)

game = {}
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
print("----------------------------------")


print(game)
