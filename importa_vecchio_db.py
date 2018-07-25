# 25.07.18
import csv
from pprint import pprint as pp
import sqlite3 as lite

from docutils.utils.punctuation_chars import delimiters

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
    """
    :return:
    dati -> {data: [t ,tmin, tmax, mm, durata]}
    """
    dati = []
    with open(DATI) as fin:
        reader = csv.reader(fin, delimiter='|')

        for rigo in reader:
            try:
                data, tmed, tmin, tmax, ur, mm, durata, press, tensvap, nuvol = rigo[1:-3]
            except ValueError:
                print(rigo)
                continue

            tmed = str2float(tmed)
            tmin = str2float(tmin)
            tmax = str2float(tmax)
            ur = str2float(ur)
            mm = str2float(mm)
            durata = str2int(durata)
            press = str2float(press)
            tensvap = str2float(tensvap)
            nuvol = str2float(nuvol)

            rec = (data, tmed, tmin, tmax, press, mm, durata, ur)

            dati.append(rec)

    return dati


def scrivi(dati):
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany("""INSERT INTO Giornaliero
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, null, null, null, null)""", dati)
