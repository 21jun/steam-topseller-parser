import odbc
from datetime import datetime
import requests
from time import sleep
from bs4 import BeautifulSoup


def date_pass():
    now = datetime.now()
    result = "%s-%s-%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return result


def get_steam_users(steam_users):
    users_cnt = []
    for i in steam_users:
        if i.string.replace(',', '').isdigit():
            users_cnt.append(i.string.replace(',', ''))
    return users_cnt


def get_id(link):
    _id = link.split('/')
    if _id[2] == 'store.steampowered.com':
        return _id[3], _id[4], _id[5]
    elif _id[2] == 'steamcommunity.com':
        return _id[3], _id[4]
    else:
        print('ERROR IN LINK')


# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()
sql = '''
    INSERT INTO oasis.player_count(title, ranking, date, current_players, peak_today, type, id_title, id_num, concurrent_steam_users, peak_steam_users) VALUES ("%s","%d","%s","%d","%d","%s","%s","%s","%d","%d")
    '''
sql_2 = '''
    INSERT INTO oasis.player_count(title, ranking, date, current_players, peak_today, type, id_num, concurrent_steam_users, peak_steam_users) VALUES ("%s","%d","%s","%d","%d","%s","%s","%d","%d")
    '''


for loop in range(0, 1000):
    url = 'https://store.steampowered.com/stats/Steam-Game-and-Player-Statistics'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    steam_users = soup.select(
        'body > div > div > div > div > div.page_content > div > div > div > div > table > tr'
    )

    data = soup.select(
        '#detailStats > table > tr.player_count_row '
    )

    games = []
    date = date_pass()

    for index, i in enumerate(data):
        link = i.find_all('a')[0].get('href')
        title = i.find_all('a')[0].string
        players = i.find_all('span')
        current_players = players[0].string.replace(',', '')
        peak_today = players[1].string.replace(',', '')
        concurrent_steam_users, peak_steam_users = get_steam_users(steam_users[1])
        id_tuple = get_id(link)
        game = {
            'current_players': int(current_players),
            'peak_today': int(peak_today),
            'title': title,
            'date': date,
            'ranking': int(index + 1),
            'concurrent_steam_users': int(concurrent_steam_users),
            'peak_steam_users': int(peak_steam_users)
        }
        if len(id_tuple) == 3:
            game['type'] = id_tuple[0]
            game['id_num'] = id_tuple[1]
            game['id_title'] = id_tuple[2]
        elif len(id_tuple) == 2:
            game['type'] = id_tuple[0]
            game['id_num'] = id_tuple[1]

        print(game)
        try:
            db.execute(sql % (
                game['title'], game['ranking'], game['date'],
                game['current_players'], game['peak_today'],
                game['type'], game['id_title'], game['id_num'],
                game['concurrent_steam_users'], game['peak_steam_users']
            ))
        except ValueError:
            print("ValueError at SQL INSERT")
        except KeyError:
            db.execute(sql_2 % (
                game['title'], game['ranking'], game['date'],
                game['current_players'], game['peak_today'],
                game['type'], game['id_num'],
                game['concurrent_steam_users'], game['peak_steam_users']
            ))
    print("---------------------------------END------------------------------------")
    sleep(300)