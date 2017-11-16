# 09.11.17: rev0

from pprint import pprint as pp

import csv_util
import db as DB
import db_util


def carica_eliofania(file_input):
    dati = csv_util.eliofania_da_sun_ephemeris(file_input, True)
    db_util.inserisci_eliofania(dati)
    pp(dati)
    print('Dati inseriti nella tabella Eliofania')


def prepopola_raw(anno):
    db_util.prepopola_raw(anno)
    print("Tabella Raw prepopolata per l'anno %i" % anno)


if __name__ == '__main__':
    pass
    # """redige bollettini per il mese indicato """
    # mese = '1710'
    # bollettino.Bollettino(mese)

    # """crea/resetta db"""
    # db = DB.DB()
    # db.crea_db()
    # db.resetta()

    # """legge i dati del file in formato csv dell'eliofania creato con il programma Sun Ephemeris e li salva
    # nella tabella Eliofania"""
    # fin = 'eliofania.csv'
    # carica_eliofania(fin)

    """Prepopola la tabella Raw"""
    anno = 2012
    prepopola_raw(anno)
