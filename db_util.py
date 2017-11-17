# 16.11.17
import datetime
import sqlite3 as lite
from pprint import pprint as pp

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


def carica_raw(dati, popola_errori=[]):
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', dati)

    if popola_errori:
        dt = datetime.timedelta(minutes=10)

        for giorno in popola_errori:
            dal = datetime.datetime.strptime(giorno, '%d/%m/%Y')
            al = dal + datetime.timedelta(days=1)

            dati = interroga('Raw', dal, al, flat=True)
            dati = [datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in dati]

            while datetime.datetime.strftime(dal,'%d/%m/%Y') == giorno:

                if not (dal in dati):
                    record = (dal, None, None, None, None, None, None, None, None, None, None)
                    cur.execute('INSERT INTO Raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', record)
                    print('%s aggiunto vuoto' % dal)

                dal+=dt

    con.commit()


def interroga(tabella, dal, al, flat=False):
    """

    :param tabella: nome della tabella
    :param dal:
    :param al:
    :param flat: se True ed è stato selezionato solo un campo, restituisce i risultati come lista
    :return:
    """
    cmd = """
    SELECT data
    FROM {tabella}
    WHERE data
    BETWEEN '{dal}' AND '{al}'
    """.format(tabella=tabella,
               dal=dal,
               al=al)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        dati = cur.execute(cmd).fetchall()

    if flat:
        dati = [x[0] for x in dati]

    return dati
