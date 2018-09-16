import odbc
import schedule
import time
import modules.PageParser_module as pp


# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()

# Loop
schedule.every().day.at("12:00").do(pp.page_parser, db)
schedule.every().day.at("00:00").do(pp.page_parser, db)
while True:
    schedule.run_pending()
    time.sleep(10)
