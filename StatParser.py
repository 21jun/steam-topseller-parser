import odbc
import time
import schedule
import modules.StatParser_module as sp

# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()


# Loop
schedule.every(5).minutes.do(sp.stat_parser, db)
while True:
    schedule.run_pending()
    time.sleep(1)
