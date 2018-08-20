# 25.07.18
import csv
import sqlite3 as lite
from pprint import pprint as pp

import pandas

from costanti import *

DATI = 'dati/stat_g.tbl'


def str2float(valore):
    if valore == '':
        return None

    return float(valore)


def str2int(valore):
    if valore == '':
        return None

    return int(valore)


def leggi_csv():
    # todo obsoleto
    """
    :return:
    dati -> {data: [t ,tmin, tmax, mm, durata]}
    """
    dati = []
    with open(DATI) as fin:
        reader = csv.reader(fin, delimiter='|')

        for rigo in reader:
            try:
                data, tmed, tmin, tmax, ur, mm, durata, press, tens, nuvol, vvel, vdir, vfil = rigo[1:]
            except ValueError:
                print(rigo)
                continue

            tmed = str2float(tmed)
            tmin = str2float(tmin)
            tmax = str2float(tmax)
            press = str2float(press)
            ur = str2float(ur)
            tens = str2float(tens)
            mm = str2float(mm)
            durata = str2int(durata)
            nuvol = str2float(nuvol)

            rec = (data, tmed, tmin, tmax, press, ur, tens, mm, durata, nuvol, vvel, vdir, vfil)

            dati.append(rec)

    return dati


def importa_csv():
    tabella = pandas.read_csv(DATI, delimiter='|', header=0, parse_dates=True, na_values=[''],
                              index_col='recno')

    dati = tabella[
        ['data', 'tmed', 'tmin', 'tmax', 'press', 'ur', 'tens', 'mm', 'durata', 'nuvol', 'vvel', 'vdir',
         'vfil']]

    with lite.connect(NOME_DB) as con:
        dati.to_sql('Annuario_Talsano_G', con, if_exists='replace', index=False)


def scrivi(dati):
    # todo obsoleto
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany("""INSERT INTO Giornaliero
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, null, null, null, null)""", dati)
