import odbc


def check():
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    db.execute("SELECT id_title, id_num FROM oasis.games")
    result = db.fetchall()

    for i in result:
        print(i)
