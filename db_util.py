# 16.11.17
import datetime
import sqlite3 as lite
from pprint import pprint as pp

import pioggia_util
import vento_util
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
            dati = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in dati]

            while datetime.datetime.strftime(dal, '%d/%m/%Y') == giorno:

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


def interroga(tabella, dal, al, campi=None, orari=False, flat=False):
    """

    :param tabella: nome della tabella
    :param dal:
    :param al:
    :param campi: elenco campi
    :param orari: seleziona solo i record registrati all'ora
    :param flat: se True ed è stato selezionato solo un campo, restituisce i risultati come lista
    :return:
    """

    if campi:
        campi = list(campi)
        campi = ', '.join(campi)
    else:
        campi = '*'

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

    piogge = pioggia_util.pioggia_per_tabella_oraria(dal, al)

    # todo: calcolare durata con piogge contigue
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Orario VALUES (?, ?, ?, ?, ?, ?, null, ?, ?, ?, ?, ?)', risultato)
        cur.executemany('UPDATE Orario SET mm = ?, durata = ? WHERE data = ?', piogge)


def calcola_tabella_Giornaliero(dal=None, al=None):
    # todo: verificare che la pioggia registrata alle ore 00.00 sia attribuita al giorno giusto
    cmd = """
    SELECT DATE(data), AVG(t), MIN(tmin), MAX(tmax), AVG(pres), SUM(mm), SUM(durata), AVG(ur), SUM(eliof), 
    SUM(pir), AVG(vvel)
    FROM Orario
    WHERE data
    BETWEEN '{dal}' AND '{al}'
    GROUP BY DATE(data)
    """.format(dal=dal, al=al)

    cmd_vento = """
    SELECT DATE(data), vvel, vdir
    FROM Raw
    WHERE data
    BETWEEN '{dal}' AND '{al}'
    """.format(dal=dal, al=al)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        dati = cur.execute(cmd).fetchall()

        dati_vento = cur.execute(cmd_vento).fetchall()
        direzione_dominante = vento_util.direzione_dominante(dati_vento, discretizzazione='giornaliero')

        cur.executemany('INSERT INTO Giornaliero VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, null)', dati)
        cur.executemany('UPDATE Giornaliero SET vdir = ? WHERE data = ?', direzione_dominante)
        cur.execute('UPDATE Giornaliero SET vdir = "-" WHERE vvel < %f' % vento_util.CALMA)


def calcola_tabella_Mensile(dal=None, al=None):
    # todo: verificare che la pioggia registrata alle ore 00.00 del primo giorno del mese sia attribuita al
    # mese giusto
    cmd = """
    SELECT strftime('%Y-%m', data), AVG(t), MIN(tmin), MAX(tmax), AVG(pres), SUM(mm), SUM(durata), AVG(ur),
           SUM(eliof), SUM(pir), AVG(vvel)
    FROM Giornaliero
    WHERE data
    BETWEEN '{dal}' AND '{al}'
    GROUP BY strftime('%Y-%m', data)
    """.format(dal=dal, al=al)

    cmd_vento = """
    SELECT strftime('%Y-%m', data), vvel, vdir
    FROM Raw
    WHERE data
    BETWEEN '{dal}' AND '{al}'
    """.format(dal=dal, al=al)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        dati = cur.execute(cmd).fetchall()
        # pp(dati)

        dati_vento = cur.execute(cmd_vento).fetchall()
        direzione_dominante = vento_util.direzione_dominante(dati_vento, discretizzazione='giornaliero')
        # pp(direzione_dominante)

        cur.executemany('INSERT INTO Mensile VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, null)', dati)
        cur.executemany('UPDATE Mensile SET vdir = ? WHERE data = ?', direzione_dominante)
        cur.execute('UPDATE Mensile SET vdir = "-" WHERE vvel < %f' % vento_util.CALMA)

def calcola_tabella_Pioggia(dal=None, al=None):
    dati = interroga('Raw', dal, al, campi=['data', 'mm'])
    pioggia = pioggia_util.Pioggia(dati)
    risultato = pioggia.calcola_pioggia(dal, al)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Pioggia VALUES (?, ?, ?, ?)', risultato)
