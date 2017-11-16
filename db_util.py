# 16.11.17
import datetime
import sqlite3 as lite

from costanti import NOME_DB


def inserisci_eliofania(dati):
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Eliofania VALUES (?, ?)', dati)


def prepopola_raw(anno):
    data = datetime.datetime(anno, 1, 1, 0)
    dt = datetime.timedelta(minutes=10)

    dati = []
    while data.year == anno:
        record = (data, None, None, None, None, None, None, None, None, None, None)
        dati.append(record)
        data += dt

    carica_raw(dati)


def carica_raw(dati):
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', dati)
