# 20.11.17: rev 0
import sqlite3 as lite
from pprint import pprint as pp

from costanti import *


class Pioggia(object):
    # todo: trasformare la classe in funzione
    def __init__(self, dati=[]):
        self.dati = dati

    def calcola_pioggia(self, dal, al):
        dati_pioggia = self.dati
        lpioggia = [(datetime.datetime.strptime(h, DATETIME_PF), mm)
                    for h, mm in dati_pioggia
                    if mm and str(dal - DT) <= h <= str(al + DT)]

        # orari_piogge = [[dalle_1, alle_1, mm1, durata1], [dalle_2, alle_2, mm2, durata2], ...]
        piogge = [[lpioggia[0][0] - DT, lpioggia[0][0], lpioggia[0][1], DT.seconds / 60], ]

        for fine, mm in lpioggia[1:]:

            if fine - DT_PIOGGIA > piogge[-1][1]:
                piogge.append([fine - DT, fine, mm, DT.seconds / 60], )
            else:
                piogge[-1][1] = fine
                piogge[-1][2] += mm
                piogge[-1][3] = (fine - piogge[-1][0]).seconds / 60

        return piogge


def pioggia_per_tabella_oraria(dal, al):
    with lite.connect(NOME_DB) as con:
        cur = con.cursor()

        # n = int(DT_PIOGGIA.seconds / 60 / 10)

        dati = []
        while dal <= al:
            cmd = """
            SELECT sum(mm)
            FROM Raw
            WHERE data
            BETWEEN datetime('{dal}', '-50 minutes') AND '{dal}'
            """.format(dal=dal)

            mm = cur.execute(cmd).fetchone()[0]

            if mm:
                cmd = """
                SELECT data, mm
                FROM Raw
                WHERE data
                BETWEEN '{da}' AND '{a}'
                AND mm > 0.0
                """.format(da=dal - DT_ORA + DT,
                           a=dal)

                risultati = cur.execute(cmd).fetchall()

                durata = len(risultati) * 10
            else:
                durata = 0

            dati.append([mm, durata, dal])

            dal += DT_ORA

    return dati


def prova():
    import db_util

    dal = datetime.datetime(2014, 1, 1)
    al = dal + datetime.timedelta(days=31)
    dati = db_util.interroga('Raw', dal, al, ['data', 'mm'])
    pioggia = Pioggia(dati)
    lpioggia = pioggia.calcola_pioggia(dal, dal + datetime.timedelta(days=1))
    pp(lpioggia)


if __name__ == '__main__':
    prova()
