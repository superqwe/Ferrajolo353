import datetime

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
NOME_DB = 'test.sqlite'
FOUT_CREA = '%i-%02i.csv'

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
