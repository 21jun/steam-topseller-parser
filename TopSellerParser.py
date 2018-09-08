import odbc
import modules.TopSellerParser_module as tp

# params
delay = 3600  # sec
repeat = 0  # count
end = False  # exit code

# db connection
connect = odbc.odbc('oasis')
db = connect.cursor()

tp.top_seller_parser(delay, end, repeat, db)
