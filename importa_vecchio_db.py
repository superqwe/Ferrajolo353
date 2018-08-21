import itertools
import sqlite3 as lite

import pandas

from costanti import *
import numpy as np

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

    for anno in range(2001, 2001 + 1):
        for mese in mesi:
            print(anno, mese)
            a = tabella[(tabella['data'] >= '2001-01-01') & (tabella['data'] < '2001-02-01')]
            print(a)
            print()
            # todo vdir
            b = a.agg({'tmed': np.mean, 'tmin': np.min, 'tmax': np.max, 'press': np.mean, 'ur': np.mean,
                       'tens': np.mean, 'mm': np.sum, 'durata': np.sum, 'nuvol': np.mean, 'vvel': np.mean,
                       #'vdir': XXX
                        'vfil': np.sum})
            print(b)
            break

            if mese == 12:
                break
        break
