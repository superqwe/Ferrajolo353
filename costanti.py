import datetime
import os

# parse/format datetime.datetime
DATETIME_PF = '%Y-%m-%d %H:%M:%S'
DATE_PF = '%Y-%m-%d'
TIME_SHORT_PF = '%H:%M'

# intervalli di tempo
DT = datetime.timedelta(minutes=10)
DT_50MIN = datetime.timedelta(minutes=50)
DT_GIORNO = datetime.timedelta(days=1)
DT_ORA = datetime.timedelta(hours=1)

# se tra un dato di pioggia rilevato ed un altro non supera questo tempo, allora la pioggia è continua
DT_PIOGGIA = datetime.timedelta(minutes=30)

# file I/O
NOME_DB = 'Annuario.sqlite'
FOUT_CREA = '%i-%02i.csv'
FOUT_ANNUARIO_GIORNI = 'annuario/tabelle_dati_giornalieri.tex'
FOUT_ANNUARIO_MESI = 'annuario/tabelle_dati_mensili.tex'
FOUT_ANNUARIO_ANNI = 'annuario/tabelle_dati_annuali.tex'
FOUT_ANNUARIO_STATISTICHE_MESI = 'annuario/tabelle_dati_statistici_mensili.tex'
FOUT_ANNUARIO_STATISTICHE_ANNI = 'annuario/tabelle_dati_statistici_annuali.tex'

# mesi
MESE = {1: 'Gennaio',
        2: 'Febbraio',
        3: 'Marzo',
        4: 'Aprile',
        5: 'Maggio',
        6: 'Giugno',
        7: 'Luglio',
        8: 'Agosto',
        9: 'Settembre',
        10: 'Ottobre',
        11: 'Novembre',
        12: 'Dicembre'}

# annuario
ANNO_INIZIO_ANNUARIO = 1975
ANNO_FINE_ANNUARIO = 2006

ANNUARIO_PATH_TEMPLATE = 'annuario/template/'

with open(os.path.join(ANNUARIO_PATH_TEMPLATE, 'tabella_dati_giornalieri.tex')) as fin:
    TABELLA_DATI_GIORNALIERI = fin.read()

with open(os.path.join(ANNUARIO_PATH_TEMPLATE, 'tabella_dati_mensili.tex')) as fin:
    TABELLA_DATI_MENSILI = fin.read()

with open(os.path.join(ANNUARIO_PATH_TEMPLATE, 'tabella_dati_annuali.tex')) as fin:
    TABELLA_DATI_ANNUALI = fin.read()

with open(os.path.join(ANNUARIO_PATH_TEMPLATE, 'tabella_dati_annuali_statistici.tex')) as fin:
    TABELLA_DATI_ANNUALI_STATISTICI = fin.read()
