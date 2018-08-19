import odbc


def check(table):
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    db.execute("SELECT id_title, id_num FROM oasis."+str(table))
    result = db.fetchall()

    for i in result:
        print(i)
