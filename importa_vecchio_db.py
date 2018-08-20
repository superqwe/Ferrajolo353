import sqlite3 as lite

import pandas

from costanti import *

DATI = 'dati/stat_g.tbl'


def importa_csv():
    tabella = pandas.read_csv(DATI, delimiter='|', header=0, parse_dates=True, na_values=[''],
                              index_col='recno')

    dati = tabella[
        ['data', 'tmed', 'tmin', 'tmax', 'press', 'ur', 'tens', 'mm', 'durata', 'nuvol', 'vvel', 'vdir',
         'vfil']]

    with lite.connect(NOME_DB) as con:
        dati.to_sql('Annuario_Talsano_G', con, if_exists='replace', index=False)
