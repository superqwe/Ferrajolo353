# 16.11.17

import sqlite3 as lite
from pprint import pprint as pp

from costanti import NOME_DB


def inserisci_eliofania(dati):
    # pp(dati)
    # db = lite.connect(NOME_DB)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Eliofania VALUES (?, ?)', dati)

    print('inseriti dati di eliofania')
