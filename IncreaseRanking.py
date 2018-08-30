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
    def __init__(self, title, st_rank, ed_rank, gap, st_date, ed_date):
        self.title = title
        self.st_rank = st_rank
        self.ed_rank = ed_rank
        self.gap = gap
        self.st_date = st_date
        self.ed_date = ed_date

    def __repr__(self):
        return repr((self.title, self.st_rank, self.ed_rank, self.gap, self.st_date, self.ed_date))


for i, game_title in enumerate(game_titles):
    db.execute(sql % game_title[0])
    games = db.fetchall()
    st = games[0]
    ed = games[len(games) - 1]
    diff = st[2] - ed[2]

    container.append(GameInfo(game_title[0], st, ed, diff, games[0][5], games[len(games)-1][5]))

result = sorted(container, key=lambda s: s.gap, reverse=True)
for index, i in enumerate(result):
    print('#', index, i.title)
    print('gap:', i.gap)
    print('st:', i.st_rank[2], '/', 'date:', i.st_date)
    print('ed:', i.ed_rank[2], '/', 'date:', i.ed_date)

    print('------------------------')