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
id_num = '552990'
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
    '#game_highlights > div > div > div.glance_ctn_responsive_left > div '
)

info2 = soup.select(
    '#game_highlights > div > div > div > div > div'
)

information = info[0]

# print(information)
a = getReviews(information.text)
print(a)
# print(information.text)
# getReview2(info[0].text)
# getReview2(info2)

# for i in information:
#     print(i)
#     print('========================================================')

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
