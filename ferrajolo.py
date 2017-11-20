# 09.11.17: rev0

from pprint import pprint as pp

import datetime

import csv_util
import db as DB
import db_util
import pioggia_util


def crea_db():
    db = DB.DB()
    db.crea_db()


def resetta_db():
    db = DB.DB()
    db.resetta()

def carica_eliofania(file_input):
    dati = csv_util.eliofania_da_sun_ephemeris(file_input, True)
    db_util.inserisci_eliofania(dati)
    pp(dati)
    print('\nDati inseriti nella tabella Eliofania')


def carica_raw(file_input, popola_errori=False):
    dati, errori = csv_util.leggi_csv(file_input)
    db_util.carica_raw(dati, popola_errori=errori)
    print('\nDati del file %s inseriti nella tabella Raw' % file_input)


def prepopola_raw(anno):
    db_util.prepopola_raw(anno)
    print("\nTabella Raw prepopolata per l'anno %i" % anno)


def ricerca_record_mancanti(dal=None, al=None, aggiungi=True):
    record = db_util.ricerca_record_mancanti(dal, al, aggiungi=aggiungi)
    print('\nElenco dei redord mancanti dal %s al %s ' % (dal, al))
    pp(record)


def calcola_tabella_Orario(dal=None, al=None):
    db_util.calcola_tabella_Orario(dal, al)
    print('\nTabella Orario popolata dal %s al %s' % (dal, al))


def calcola_tabella_Giornaliero(dal=None, al=None):
    db_util.calcola_tabella_Giornaliero(dal, al)
    print('\nTabella Giornaliero popolata dal %s al %s' % (dal, al))


def calcola_tabella_Pioggia(dal, al):
    db_util.calcola_tabella_Pioggia(dal, al)
    print('\nTabella Pioggia popolata dal %s al %s' % (dal, al))

if __name__ == '__main__':
    # """redige bollettini per il mese indicato."""
    # mese = '1710'
    # bollettino.Bollettino(mese)

    # """crea/resetta db"""
    # crea_db()
    # resetta_db()

    # """legge i dati del file in formato csv dell'eliofania creato con il programma Sun Ephemeris e li salva
    # nella tabella Eliofania."""
    # fin = 'eliofania.csv'
    # carica_eliofania(fin)

    # """carica i dati dal file nella tabella Raw. Il file deve essere salvato nella cartella 'dati'.
    # popola_errori == True --> popola con record vuoti i giorni che hanno avuto problemi durante il caricamento
    # """
    # fin = '2016a.txt'
    # carica_raw(fin, popola_errori=False)

    # """Prepopola la tabella Raw"""
    # anno = 2018
    # prepopola_raw(anno)

    # """Ricerca record mancanti"""
    # dal = datetime.datetime(2012, 1, 1, 1, 10)
    # al = datetime.datetime(2016, 12, 31, 23, 59)
    # ricerca_record_mancanti(dal, al, aggiungi=True)

    """Popola la tabella Orario dai dati della tabella Raw"""
    dal = datetime.datetime(2016, 1, 1)
    al = datetime.datetime(2016, 1, 4)
    calcola_tabella_Orario(dal, al)

    # """Popola la tabella Giornaliero dai dati della tabella Raw (vvel, vdir, mm) ed Orario"""
    # dal = datetime.datetime(2016, 1, 1)
    # al = datetime.datetime(2017, 1, 1)
    # calcola_tabella_Giornaliero(dal, al)

    # """Popola la tabella Pioggia"""
    # dal = datetime.datetime(2016, 1, 1)
    # al = datetime.datetime(2017, 1, 1)
    # calcola_tabella_Pioggia(dal, al)


    pass
