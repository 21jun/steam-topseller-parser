import odbc
import matplotlib.pyplot as plt

# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()
db.execute("select current_players, date from oasis.player_count where title like '%PLAYERUNKNOWN%'")
result = db.fetchall()

players = []
date = []
for re in result:
    players.append(re[0])
    date.append(re[1])
plt.plot(date, players, 'r--')

plt.show()
