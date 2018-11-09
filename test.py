import odbc
import datetime

# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()
db.execute("select ranking,title,(current_players), peak_today, date from oasis.player_count ")
result = db.fetchall()

db.execute("select title from oasis.player_count group by title")
tt = db.fetchall()

info = []
titles = []

for re in result:
    info.append({
        'current_players': re[2],
        'ranking': re[0],
        'title': re[1],
        'date': re[4]
    })

for t in tt:
    titles.append(t[0])

weekday = {
    'Monday': 0,
    'Tuesday': 0,
    'Wednesday': 0,
    'Thursday': 0,
    'Friday': 0,
    'Saturday': 0,
    'Sunday': 0
}

counts = []
top100 = []
game = []

for t in titles:
    min_player = 9999999
    max_player = 0

    sum_player = 0
    avg_player = 0

    cnt = 0

    min_ranking = 101
    max_ranking = 0

    max_weekday = -1
    min_weekday = -1

    weekday_sum = {
        'Monday': {
            'cnt': 0,
            'players': 0
        },
        'Tuesday': {
            'cnt': 0,
            'players': 0
        },
        'Wednesday': {
            'cnt': 0,
            'players': 0
        },
        'Thursday': {
            'cnt': 0,
            'players': 0
        },
        'Friday': {
            'cnt': 0,
            'players': 0
        },
        'Saturday': {
            'cnt': 0,
            'players': 0
        },
        'Sunday': {
            'cnt': 0,
            'players': 0
        }
    }

    for i in info:
        if t == i['title']:
            cnt += 1
            sum_player += int(i['current_players'])
            if max_player < int(i['current_players']):
                max_player = int(i['current_players'])
                max_weekday = i['date'].strftime("%A")
            if min_player > int(i['current_players']):
                min_player = int(i['current_players'])
                min_weekday = i['date'].strftime("%A")
            if min_ranking > int(i['ranking']):
                min_ranking = int(i['ranking'])
            if max_ranking < int(i['ranking']):
                max_ranking = int(i['ranking'])
            weekday_sum[i['date'].strftime("%A")]['players'] += int(i['current_players'])
            weekday_sum[i['date'].strftime("%A")]['cnt'] += 1

        else:
            pass

    if cnt == 0:
        continue

    for i in weekday_sum.values():
        if i['cnt'] == 0:
            i['cnt'] = 1

    avg_player = sum_player / cnt
    gap_player = max_player - min_player
    gap_ranking = max_ranking - min_ranking

    if (weekday_sum['Monday']['players'] == 0 or weekday_sum['Tuesday']['players'] == 0 or weekday_sum['Wednesday'][
        'players'] == 0 or
            weekday_sum['Thursday']['players'] == 0 or weekday_sum['Friday']['players'] == 0 or weekday_sum['Saturday'][
                'players'] == 0 or weekday_sum['Sunday']['players'] == 0):
        continue

    workday = (weekday_sum['Monday']['players'] / weekday_sum['Monday']['cnt'] +
               weekday_sum['Tuesday']['players'] / weekday_sum['Tuesday']['cnt'] +
               weekday_sum['Wednesday']['players'] / weekday_sum['Wednesday']['cnt'] +
               weekday_sum['Thursday']['players'] / weekday_sum['Thursday']['cnt'] +
               weekday_sum['Friday']['players'] / weekday_sum['Friday']['cnt']) / 5
    weekend = (weekday_sum['Saturday']['players'] / weekday_sum['Saturday']['cnt'] +
               weekday_sum['Sunday']['players'] / weekday_sum['Sunday']['cnt']) / 2

    game.append({
        'title': t,
        'top_rank': min_ranking,
        'week_avg': {
            'Monday': weekday_sum['Monday']['players'] / weekday_sum['Monday']['cnt'],
            'Tuesday': weekday_sum['Tuesday']['players'] / weekday_sum['Tuesday']['cnt'],
            'Wednesday': weekday_sum['Wednesday']['players'] / weekday_sum['Wednesday']['cnt'],
            'Thursday': weekday_sum['Thursday']['players'] / weekday_sum['Thursday']['cnt'],
            'Friday': weekday_sum['Friday']['players'] / weekday_sum['Friday']['cnt'],
            'Saturday': weekday_sum['Saturday']['players'] / weekday_sum['Saturday']['cnt'],
            'Sunday': weekday_sum['Sunday']['players'] / weekday_sum['Sunday']['cnt']
        },
        'avg_player': avg_player,
        'ratio': weekend / workday
    })
    # print(t, weekend, workday)

for i in game:

    if i['ratio']:
        print(i)
        db.execute(
            '''INSERT INTO oasis.wed_thu(title, top_rank, avg_player, ratio ,Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) 
            VALUES ("%s","%d","%lf","%lf","%lf","%lf","%lf","%lf","%lf","%lf","%lf")''' % (
                i['title'], i['top_rank'], i['avg_player'], i['ratio'], i['week_avg']['Monday'],
                i['week_avg']['Tuesday'],
                i['week_avg']['Wednesday'], i['week_avg']['Thursday'], i['week_avg']['Friday'],
                i['week_avg']['Saturday'], i['week_avg']['Sunday']))

    #
    #
    # for i in range(len(top100) - 1):
    #     for j in range(len(top100) - i - 1):
    #         if top100[j]['avg_player'] < top100[j + 1]['avg_player']:
    #             top100[j], top100[j + 1] = top100[j + 1], top100[j]
    #
    # for i in top100:
    #     db.execute('''INSERT INTO oasis.top100(title, top_rank, avg_player) VALUES ("%s","%d","%lf")''' % (
    #     i['title'], i['top_rank'], i['avg_player']))
    #     print("%s\ntop_rank:%3d avg_player:%6.2f" % (i['title'], i['top_rank'], i['avg_player']))
    #     print("====================================")
