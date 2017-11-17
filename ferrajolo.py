# 09.11.17: rev0

from pprint import pprint as pp

import datetime

import csv_util
import db as DB
import db_util


def carica_eliofania(file_input):
    dati = csv_util.eliofania_da_sun_ephemeris(file_input, True)
    db_util.inserisci_eliofania(dati)
    pp(dati)
    print('Dati inseriti nella tabella Eliofania')


def carica_raw(file_input, popola_errori=False):
    dati, errori = csv_util.leggi_csv(file_input)
    db_util.carica_raw(dati, popola_errori=errori)
    print('Dati del file %s inseriti nella tabella Raw' % file_input)


def prepopola_raw(anno):
    db_util.prepopola_raw(anno)
    print("Tabella Raw prepopolata per l'anno %i" % anno)


def ricerca_record_mancanti(dal=None, al=None, aggiungi=True):
    record = db_util.ricerca_record_mancanti(dal, al, aggiungi=aggiungi)
    print('Elenco dei redord mancanti dal %s -- %s ' % (dal, al))
    pp(record)

if __name__ == '__main__':
    # """redige bollettini per il mese indicato."""
    # mese = '1710'
    # bollettino.Bollettino(mese)

    # """crea/resetta db"""
    db = DB.DB()
    # db.crea_db()
    # db.resetta()

    # """legge i dati del file in formato csv dell'eliofania creato con il programma Sun Ephemeris e li salva
    # nella tabella Eliofania."""
    # fin = 'eliofania.csv'
    # carica_eliofania(fin)

    # """carica i dati dal file nella tabella Raw. Il file deve essere salvato nella cartella 'dati'.
    # popola_errori == True --> popola con record vuoti i giorni che hanno avuto problemi durante il caricamento
    # """
    # fin = '2016a.txt'
    # carica_raw(fin, popola_errori=True)

    # """Prepopola la tabella Raw"""
    # anno = 2018
    # prepopola_raw(anno)

    """Ricerca record mancanti"""
    dal = datetime.datetime(2012, 1, 1, 1, 10)
    al = datetime.datetime(2016, 12, 31, 23, 59)
    ricerca_record_mancanti(dal, al, aggiungi=True)



    pass
