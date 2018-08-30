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
    def __init__(self, title, rank_avg):
        self.title = title
        self.rank_avg = rank_avg

    def __repr__(self):
        return repr((self.title, self.rank_avg))


for i, game_title in enumerate(game_titles):
    db.execute(sql % game_title[0])
    games = db.fetchall()

    rank_sum = 0
    for game in games:
        rank_sum += game[2]
    rank_avg = rank_sum / len(games)

    container.append(GameInfo(game_title[0], rank_avg))

result = sorted(container, key=lambda s: s.rank_avg, reverse=False)
sql = '''select * from '''
for index, i in enumerate(result):
    if i.rank_avg > 100:
        continue
    print('#', index, i.title)
    print('rank_avg', i.rank_avg)

    print('------------------------')
