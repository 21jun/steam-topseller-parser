import odbc
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup


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

def getReview2(info):
    print(info[0])


def cleanStr(str):
    result = str.replace('\t', '')
    result = result.replace('\r', '')
    result = result.replace('\n', ' ')
    # result = result.replace('  ', '')
    # result = result.replace(' ','')
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


id_title = ''
id_num = '359550'
type = 'app'

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
# game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div > div:nth-child(1) > div.summary.column > span.game_review_summary
# game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div > div:nth-child(1) > div.summary.column > span.game_review_summary.positive
# game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div > div:nth-child(2) > div.summary.column > span.responsive_hidden
recent_review = soup.select(
    '#game_highlights > div > div > div > div > div > div > span'
)
# game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div
info = soup.select(
    '#game_highlights > div > div > div.glance_ctn_responsive_left > div'
)

info2 = soup.select(
    '#game_highlights > div > div > div > div > div'
)

information = info[0]

#print(information)


#getReview2(info[0])
#getReview2(info2)

for i in information:
    print(i)
    print('========================================================')

# print(len(info))
# print(len(info2))
#
# for i in info2:
#     print(i)
#     print('---------------------')

# print(info[0])
# print(len(info[0]))
# a = getReviews(info)
# print(a)
#
# if('Recent'in rrr[0]):
#     print("--Recent Reviews--")
#     for i in rrr:
#         print(i)
#     print("--All Reviews--")
#     for i in rrr:
#         print(i)
#
# if('All' in rrr[0]):
#     print("--All Reviews--")
#     for i in rrr:
#         print(i)
# print(rrr[0])
# print(rrr[1])
# print(rrr[2])


# print(reviews[0].text)
# print(reviews[1].text)
#
# print(reviews[3].text)
# print(reviews[4].text)

# dev = info[0].find_all("div")
# print(cleanStr(dev[1].text))
# print(cleanStr(info[0].text))


# if (ageCheck or contentWarning):
#
#     print("age check")
#     print("----------------------------------")
# else:
#     print(id_title)
#     getReview(recent_review)


# print(id_title)
# if (recent_review):
#     print(recent_review[0].text)
#     print(cleanStr(recent_review[1].text))
# if (developer):
#     print((developer[0].text))
# if (publisher):
#     print(publisher[1].text)
# if (tags):
#     print(cleanStr(tags[0].text))
# print("----------------------------------")
