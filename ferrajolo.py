import itertools
from pprint import pprint as pp

import annuario
import bollettino_util
import csv_util
import db as DB
import db_util
import grafici
import importa_vecchio_db
from costanti import *


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


def carica_raw(file_input):
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


def calcola_tabella_orario(dal=None, al=None):
    db_util.calcola_tabella_orario(dal, al)
    print('\nTabella Orario popolata dal %s al %s' % (dal, al))


def calcola_tabella_giornaliero(dal=None, al=None):
    db_util.calcola_tabella_giornaliero(dal, al)
    print('\nTabella Giornaliero popolata dal %s al %s' % (dal, al))


def calcola_tabella_mensile(dal, al):
    db_util.calcola_tabella_mensile(dal, al)
    print('\nTabella Mensile popolata dal %s al %s' % (dal, al))


def calcola_tabella_annuale(dal, al):
    db_util.calcola_tabella_annuale(dal, al)
    print('\nTabella Annuale popolata dal %s al %s' % (dal, al))


def calcola_tabella_pioggia(dal, al):
    db_util.calcola_tabella_pioggia(dal, al)
    print('\nTabella Pioggia popolata dal %s al %s' % (dal, al))


def bollettino_crea(anno, mese):
    bollettino = bollettino_util.Bollettino(anno, mese)
    bollettino.crea_tabella()
    bollettino.crea_xls()
    print('%i-%02i.csv scritto' % (anno, mese))


def bollettino_mensile(anno, mese):
    bollettino = bollettino_util.Bollettino(anno, mese)
    bollettino.mensile_tabella()
    # bollettino.mensile_pdf()
    print('%i-%02i Mensile.pdf scritto' % (anno, mese))


def importa_vecchi_dati():
    importa_vecchio_db.importa_csv()


class talsano(object):
    def __init__(self):
        # resetta_db()
        # importa_vecchi_dati()

        self.annuario_talsano = annuario.annuario_talsano()

        self.latex()
        # self.grafici()

    def latex(self):
        # self._latex_dati_giornalieri()
        # self._latex_dati_mensili()
        self._latex_dati_annuali()

    def _latex_dati_giornalieri(self):
        mesi = itertools.cycle(range(1, 12 + 1))

        with open(FOUT_ANNUARIO_GIORNI, 'w') as fout:

            for anno in range(ANNO_INIZIO_ANNUARIO, ANNO_FINE_ANNUARIO + 1):

                for mese in mesi:
                    tex = self.annuario_talsano.latex_dati_giornalieri(mese, anno)
                    fout.write(tex)

                    if mese == 12:
                        break

    def _latex_dati_mensili(self):
        with open(FOUT_ANNUARIO_MESI, 'w') as fout:
            for anno in range(ANNO_INIZIO_ANNUARIO, ANNO_FINE_ANNUARIO + 1, 2):
                tex = self.annuario_talsano.latex_dati_mensili(anno)
                fout.write(tex)

    def _latex_dati_annuali(self):
        tex = self.annuario_talsano.latex_dati_anni()

        # tabella dati
        with open(FOUT_ANNUARIO_ANNI, 'w') as fout:
            fout.write(tex[0])

        # tabella statistiche
        with open(FOUT_ANNUARIO_STATISTICHE_ANNI, 'w') as fout:
            fout.write(tex[1])

    def grafici(self):
        # grafici temperature
        # todo aggiungere grafico escursione giornaliera
        grafici.annuario_t_mese2(self.annuario_talsano.t_mese)
        grafici.annuario_t_anno2(self.annuario_talsano.t_anno)

        # # grafici pioggia
        # grafici.annuario_p_anno(self.annuario_talsano.p_anno)
        # grafici.annuario_p_mese(self.annuario_talsano.p_mese)
        #
        # grafici.annuario_pg_anno(self.annuario_talsano.pg_anno)
        # grafici.annuario_pg_mese(self.annuario_talsano.pg_mese)
        #
        # grafici.annuario_pf_anno(self.annuario_talsano.pf_anno)


if __name__ == '__main__':
    # """redige bollettini per il mese indicato."""
    # mese = '1710'
    # bollettino.Bollettino(mese)

    """crea/resetta db"""
    # crea_db()
    # resetta_db()

    # """legge i dati del file in formato csv dell'eliofania creato con il programma Sun Ephemeris e li salva
    # nella tabella Eliofania."""
    # fin = 'eliofania.csv'
    # carica_eliofania(fin)

    """carica i dati dal file nella tabella Raw. Il file deve essere salvato nella cartella 'dati'.
    popola_errori == True --> popola con record vuoti i giorni che hanno avuto problemi durante il caricamento
    """
    # fin = '2016a.txt'
    # carica_raw(fin)

    # for x in range(2, 7):
    #     fin = '201%ia.txt' % x
    #     carica_raw(fin)

    # """Prepopola la tabella Raw"""
    # anno = 2018
    # prepopola_raw(anno)

    # """Ricerca record mancanti"""
    # dal = datetime.datetime(2012, 1, 1, 1, 10)
    # al = datetime.datetime(2016, 12, 31, 23, 59)
    # ricerca_record_mancanti(dal, al, aggiungi=True)

    """Popola la tabella Orario dai dati della tabella Raw"""
    # dal = datetime.datetime(2016, 1, 1)
    # al = datetime.datetime(2016, 2, 1)
    # calcola_tabella_orario(dal, al)

    """Popola la tabella Giornaliero dai dati della tabella Raw (vvel, vdir, mm) ed Orario"""
    # dal = datetime.datetime(2016, 1, 1)
    # al = datetime.datetime(2017, 1, 1)
    # calcola_tabella_giornaliero(dal, al)

    """Popola la tabella Mensile dai dati della tabella Raw (vvel, vdir) e Giornaliero"""
    # dal = datetime.datetime(1975, 1, 1)
    # al = datetime.datetime(2007, 1, 1)
    # calcola_tabella_mensile(dal, al)

    """Popola la tabella Annuale dai dati della tabella Raw (vvel, vdir) e Mensile"""
    # dal = datetime.datetime(2016, 1, 1)
    # al = datetime.datetime(2017, 1, 1)
    # calcola_tabella_annuale(dal, al)

    # """Popola la tabella Pioggia"""
    # dal = datetime.datetime(2012, 1, 1)
    # al = datetime.datetime(2017, 1, 1)
    # calcola_tabella_pioggia(dal, al)

    """Bollettino CREA"""
    # anno = 2016
    # mese = 1
    # bollettino = bollettino_crea(anno, mese)

    """Bollettino Mensile"""
    # anno = 2016
    # mese = 1
    # bollettino = bollettino_mensile(anno, mese)

    """Annuaario Talsano"""
    talsano()
