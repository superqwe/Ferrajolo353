# 16.11.17
import datetime
import sqlite3 as lite
from pprint import pprint as pp

from costanti import *


def inserisci_eliofania(dati):
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Eliofania VALUES (?, ?)', dati)


def prepopola_raw(anno):
    data = datetime.datetime(anno, 1, 1, 0)

    dati = []
    while data.year == anno:
        record = (data, None, None, None, None, None, None, None, None, None, None)
        dati.append(record)
        data += DT

    carica_raw(dati)


def carica_raw(dati, popola_errori=[]):
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', dati)

    if popola_errori:

        for giorno in popola_errori:
            dal = datetime.datetime.strptime(giorno, '%d/%m/%Y')
            al = dal + datetime.timedelta(days=1)

            dati = interroga('Raw', dal, al, flat=True)
            dati = [datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in dati]

            while datetime.datetime.strftime(dal,'%d/%m/%Y') == giorno:

                if not (dal in dati):
                    aggiungi_record_vuoto(cur, dal)

                dal += DT

    con.commit()


def aggiungi_record_vuoto(cur, data):
    record = (data, None, None, None, None, None, None, None, None, None, None)
    cur.execute('INSERT INTO Raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', record)
    print('%s aggiunto vuoto' % data)


def ricerca_record_mancanti(dal=None, al=None, aggiungi=False):
    dati = interroga('Raw', dal, al, flat=True)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        record_mancanti = []
        while dal <= al:

            try:
                dati.remove(datetime.datetime.strftime(dal, '%Y-%m-%d %H:%M:%S'))
            except ValueError:
                record_mancanti.append(dal)

                if aggiungi:
                    aggiungi_record_vuoto(cur, dal)

            dal += DT

        con.commit()

    return record_mancanti


def interroga(tabella, dal, al, campi='data', orari=False, flat=False):
    """

    :param tabella: nome della tabella
    :param dal:
    :param al:
    :param campi: elenco campi
    :param orari: seleziona solo i record registrati all'ora
    :param flat: se True ed è stato selezionato solo un campo, restituisce i risultati come lista
    :return:
    """

    orari = """AND (strftime('%M', data) = '00')""" if orari else ''

    cmd = """
    SELECT {campi}
    FROM {tabella}
    WHERE data
    BETWEEN '{dal}' AND '{al}'
    {orari}
    """.format(campi=campi,
               tabella=tabella,
               dal=dal,
               al=al,
               orari=orari)

    # print(cmd)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        dati = cur.execute(cmd).fetchall()

    if flat:
        dati = [x[0] for x in dati]

    return dati


def calcola_tabella_Orario(dal=None, al=None):
    risultato = interroga('Raw', dal, al, campi='*', orari=True)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Orario VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', risultato)
