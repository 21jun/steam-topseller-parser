import odbc
import modules.StatParser_module as sp

# params
end = False
repeat = 0
delay = 10.0  # sec
# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()

sp.player_parser(delay, False, repeat, db)
