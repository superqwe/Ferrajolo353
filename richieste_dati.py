# 12.01.18
import datetime
import sqlite3 as lite
from costanti import *
from pprint import pprint as pp


def ciccio():
    """
    12.01.18
    Avv.
    condizioni meteo generali 16.10.16
    vento 07.10.16
    """
    data1 = datetime.datetime(2016, 7, 16)
    data2 = datetime.datetime(2016, 10, 16)

    cmd2 = """
        SELECT *
        FROM Giornaliero
        WHERE data = "{data2}"
        """.format(data2=data2.date())

    print(cmd2)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        dati2 = cur.execute(cmd2).fetchall()
        pp(dati2)


if __name__ == '__main__':
    ciccio()
