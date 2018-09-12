import odbc
import matplotlib.pyplot as plt

# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()
db.execute("select current_players from oasis.player_count where title like '%PLAYERUNKNOWN%' ")
players = db.fetchall()

db.execute("select date from oasis.player_count where title like '%PLAYERUNKNOWN%' ")
date = db.fetchall()

plt.plot(players, 'r--')

plt.show()
