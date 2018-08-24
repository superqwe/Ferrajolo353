import calendar
import itertools
import sqlite3 as lite
from pprint import pprint as pp

import numpy as np
import pandas

import vento_util
from costanti import *

DATI = 'dati/stat_g.tbl'


def importa_csv():
    # tabella giornaliera
    print('Tabella Giornaliera')
    tabella = pandas.read_csv(DATI, delimiter='|', header=0, parse_dates=True, na_values=[''],
                              index_col='recno')

    dati = tabella[
        ['data', 'tmed', 'tmin', 'tmax', 'press', 'ur', 'tens', 'mm', 'durata', 'nuvol', 'vvel', 'vdir',
         'vfil']]

    dati['press'] = (dati['press'] + 700) * 1.33322387415

    with lite.connect(NOME_DB) as con:
        dati.to_sql('Annuario_Talsano_G', con, if_exists='replace', index=False)

    # tabella mensile
    print('\nTabella Mensile')

    mesi = itertools.cycle(range(1, 12 + 1))

    dati_mensili = []
    for anno in range(1975, 2006 + 1):
        for mese in mesi:
            gg = calendar.monthrange(anno, mese)[1]
            dal = datetime.date(anno, mese, 1)
            al = datetime.date(anno, mese, gg)

            dati = tabella[(tabella['data'] >= '%s' % dal) & (tabella['data'] <= '%s' % al)]
            dati['press'] = (dati['press'] + 700) * 1.33322387415
            
            # todo  da fare così
            # b = dati.agg({'tmed': np.mean, 'tmin': np.min, 'tmax': np.max, 'press': np.mean, 'ur': np.mean,
            #            'tens': np.mean, 'mm': np.sum, 'durata': np.sum, 'nuvol': np.mean, 'vvel': np.mean,
            #            #'vdir': XXX
            #             'vfil': np.sum})

            tmed = np.mean(dati.tmed)
            tmin = np.min(dati.tmin)
            tmax = np.max(dati.tmax)
            press = np.mean(dati.press)
            ur = np.mean(dati.ur)
            tens = np.mean(dati.tens)
            mm = np.sum(dati.mm)
            durata = np.sum(dati.durata)
            nuvol = np.mean(dati.nuvol)
            vvel = np.mean(dati.vvel)
            # todo vdir: prendere i dati orari
            vdir = vento_util.vento_con_settori(dati[['vdir']]).dominante
            vfil = np.sum(dati.vfil)

            rec = (dal, tmed, tmin, tmax, press, ur, tens, mm, durata, nuvol, vvel, vdir, vfil)
            dati_mensili.append(rec)

            # break

            if mese == 12:
                break
        # break

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Annuario_Talsano_M VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        dati_mensili)

    # tabella annuale
    print('\nTabella Annuale')

    dati_annuali = []
    for anno in range(1975, 2006 + 1):
        dal = datetime.date(anno, 1, 1)
        al = datetime.date(anno, 12, 31)

        dati = tabella[(tabella['data'] >= '%s' % dal) & (tabella['data'] <= '%s' % al)]
        dati['press'] = (dati['press'] + 700) * 1.33322387415
        
        tmed = np.mean(dati.tmed)
        tmin = np.min(dati.tmin)
        tmax = np.max(dati.tmax)
        press = np.mean(dati.press)
        ur = np.mean(dati.ur)
        tens = np.mean(dati.tens)
        mm = np.sum(dati.mm)
        durata = np.sum(dati.durata)
        nuvol = np.mean(dati.nuvol)
        vvel = np.mean(dati.vvel)
        # todo vdir: prendere i dati orari
        vdir = vento_util.vento_con_settori(dati[['vdir']]).dominante
        vfil = np.sum(dati.vfil)

        rec = (anno, tmed, tmin, tmax, press, ur, tens, mm, durata, nuvol, vvel, vdir, vfil)
        dati_annuali.append(rec)

        # break

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        cur.executemany('INSERT INTO Annuario_Talsano_A VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        dati_annuali)
