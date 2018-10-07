import requests
from bs4 import BeautifulSoup
import threading
import Checker
import modules.DateFormatter as DatePass
import time

date = DatePass.date_pass()
sql = '''
    INSERT INTO oasis.games(title, ranking, price, price_discounted, date, release_date, type, id_title, id_num) VALUES ("%s","%d","%d","%d","%s","%s","%s","%s","%s")
    '''

repeat = 0


def month_converter(month):
    return {
        'JAN': '1',
        'FEB': '2',
        'MAR': '3',
        'APR': '4',
        'MAY': '5',
        'JUN': '6',
        'JUL': '7',
        'AUG': '8',
        'SEP': '9',
        'OCT': '10',
        'NOV': '11',
        'DEC': '12'
    }[month]


def clean_date(date):
    try:
        if date == '':
            return '0000-00-00'
        date = date.replace(',', '')
        date = date.replace('.', '')
        date = date.split(' ')
        if len(date) < 3:
            return '0000-00-00'
        if 'th' in date[1]:
            result = date[2] + '-' + month_converter(date[0][0:3].upper()) + '-' + date[1].replace('th', '')
        elif date[1].isdigit():
            result = date[2] + '-' + month_converter(date[0].upper()) + '-' + date[1]
        else:
            result = date[2] + '-' + month_converter(date[1].upper()) + '-' + date[0]
        return result
    except:
        return '0000-00-00'

def clean_str(str, isDiscounted):
    result = str.replace('\t', '')
    result = result.replace('\r', '')
    result = result.replace('\n', '')
    result = result.replace('₩', '')
    result = result.replace(',', '')
    if result == '':
        return 0
    result = result.split()
    if len(result) == 2 and isDiscounted:
        if result[1] == 'Free':
            return 0
        elif not result[1].isdigit():
            return 0
        return int(result[1])  # return discounted price
    else:
        if result[0] == 'Free':
            return 0
        elif not result[0].isdigit():
            return 0
        return int(result[0])  # return original price


def clean_id(id, isTitle):
    result = id.get('href')
    if not isTitle:
        return result.split('/')[4]  # return id_num (number)
    elif result.split('/')[3] == 'app':
        return result.split('/')[5]  # return id_title (string)
    else:
        return 'NONE'


def top_seller_parser(db):
    global repeat
    try:
        repeat += 1
        games = []
        # TODO
        print("[START]")
        for page in range(1, 41):
            # sleep(0.1)
            date = DatePass.date_pass()
            # parsing
            url = 'https://store.steampowered.com/search/?category1=998&filter=topsellers&page=' + str(page)
            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            titles = soup.select(
                'div.responsive_search_name_combined > div.col.search_name.ellipsis > span'
            )
            release_dates = soup.select(
                'div.responsive_search_name_combined > div.col.search_released.responsive_secondrow'
            )
            prices = soup.select(
                'div.responsive_search_name_combined > div.col.search_price_discount_combined.responsive_secondrow > div.col.search_price.responsive_secondrow'
            )
            links = soup.select(
                '#search_result_container > div > a'
            )

            # print(soup)
            for i in range(0, 25):
                # print(page)
                games.append({'rank': int(i + 1 + (page - 1) * 25),
                              'title': titles[i].text.replace('\"', "'"),
                              'release': clean_date(release_dates[i].text),
                              'date': date,
                              'price': (clean_str(prices[i].text, False)),
                              'price_discounted': (clean_str(prices[i].text, True)),
                              'id_num': clean_id(links[i], False),
                              'id_title': clean_id(links[i], True),
                              'type': links[i].get('href').split('/')[3]})
                # print(games)
        for i in range(0, 1000):
            print(
                games[i]['rank'],
                games[i]['title'],
                games[i]['release'],
                games[i]['date'],
                games[i]['price'],
                games[i]['price_discounted'],
                games[i]['id_num'],
                games[i]['id_title'],
                games[i]['type'])

        for i in range(0, 1000):
            print(games[i]['title'])
            try:
                db.execute(sql % (
                    games[i]['title'], games[i]['rank'], games[i]['price'], games[i]['price_discounted'],
                    games[i]['date'],
                    games[i]['release'], games[i]['type'], games[i]['id_title'], games[i]['id_num']))
            except:
                print("UNICODE PROBLEM")
                db.execute(sql % (
                    "NONE", games[i]['rank'], games[i]['price'], games[i]['price_discounted'], games[i]['date'],
                    games[i]['release'], games[i]['type'], games[i]['id_title'], games[i]['id_num']))

        Checker.check('games')
        print("---------------------------------", "[", repeat, "]", "------------------------------------")
    except:
        print("ERROR OCCUR")
        print("---------------------------------", "[", repeat, "]", "------------------------------------")
