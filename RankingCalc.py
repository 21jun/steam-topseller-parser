import odbc

connect = odbc.odbc('oasis')
db = connect.cursor()

db.execute('''select MAX(title) from oasis.games group by id_title''')
game_titles = db.fetchall()

sql = '''select * from oasis.games where title LIKE "%s" '''
gap = 0
most_increase = ''

container = []
gaps = []


class GameInfo:
    def __init__(self, title, min_rank, max_rank, gap, date_rank_max, date_rank_min):
        self.title = title
        self.min_rank = min_rank
        self.max_rank = max_rank
        self.gap = gap
        self.date_max = date_rank_max
        self.date_min = date_rank_min

    def __repr__(self):
        return repr((self.title, self.min_rank, self.max_rank, self.gap, self.date_max, self.date_min))


# for game_title in game_titles:
#     db.execute(sql % game_title[0])
#     games = db.fetchall()
#
#     info = {}
#     for game in games:
#         info['title'] = game_title[0]
#         info['st_rank'] = game[2]
#         info['ed_rank'] = game[2]
#
#     for game in games:
#         info['ed_rank'] = game[2]
#     info['gap'] = info['st_rank'] - info['ed_rank']
#
#     container.append(info)
#
# for i in container:
#     if i['ed_rank'] <= 100:
#         print(i)

# for game_title in game_titles:
#     db.execute(sql % game_title[0])
#     games = db.fetchall()
#
#     flag = True
#
#     for game in games:
#         if game[2] > 100:
#             flag = False
#             break
#     if flag:
#         print(game_title[0])


for i, game_title in enumerate(game_titles):
    db.execute(sql % game_title[0])
    games = db.fetchall()
    # print(games)
    minRank = 1000
    maxRank = 1

    date_rank_max = 0
    date_rank_min = 0
    info = {}

    for game in games:
        if minRank > game[2]:
            minRank = game[2]
            date_rank_min = game[5]
        if maxRank < game[2]:
            maxRank = game[2]
            date_rank_max = game[5]

    container.append(GameInfo(game_title[0], minRank, maxRank, maxRank - minRank, date_rank_max, date_rank_min))

    # print(i, game_title[0], minRank, maxRank, maxRank - minRank)
result = sorted(container, key=lambda s: s.gap, reverse=True)
for index, i in enumerate(result):
    print('#', index, i.title)
    print('gap:', i.gap)
    print('min:', i.min_rank, '/', 'date:', i.date_min)
    print('max:', i.max_rank, '/', 'date:', i.date_max)

    print('------------------------')
