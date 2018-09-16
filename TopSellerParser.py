import odbc
import schedule
import time
import modules.TopSellerParser_module as tp


# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()

# Loop
schedule.every(2).hours.do(tp.top_seller_parser, db)
while True:
    schedule.run_pending()
    time.sleep(10)



