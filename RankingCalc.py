import odbc

connect = odbc.odbc('oasis')
db = connect.cursor()

db.execute('''select MAX(title) from oasis.games group by id_title''')
game_titles = db.fetchall()

sql = '''select * from oasis.games where title LIKE "%s" '''
gap = 0
most_increase = ''
for game_title in game_titles:
    db.execute(sql % game_title[0])
    games = db.fetchall()
    # print(games)
    minRank = 1000
    maxRank = 1

    for game in games:
        if minRank > game[2]:
            minRank = game[2]
        if maxRank < game[2]:
            maxRank = game[2]

    if gap < maxRank - minRank:
        gap = maxRank - minRank
        most_increase = game_title[0]
    print(game_title[0], minRank, maxRank)


print(gap)
print(most_increase)
