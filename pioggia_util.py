# 20.11.17: rev 0
import sqlite3 as lite
from pprint import pprint as pp

import util
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
    """
    Calcola la pioggia caduta nell'ora
    :param dal:
    :param al:
    :return: [[mm1, durata1, pioggia_nell_ora1], ...]
    daurata è in minuti
    pioggia_nell_ora è datetime.datetime
    """

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()

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
                durata = durata_pioggia(cur, dal - DT_50MIN, dal)
                # print('mm', '%5.1f' % mm, dal, durata)
            else:
                durata = 0

            dati.append([mm, durata, dal])

            dal += DT_ORA

    return dati


def durata_pioggia(cur, dal, al):
    cmd = """
    SELECT dalle, alle
    FROM Pioggia
    WHERE (dalle >= '{dal}' AND alle <= '{al}') OR 
          (dalle <= '{dal}' AND alle >= '{dal}')
    """.format(dal=dal,
               al=al)

    lista_piogge = cur.execute(cmd).fetchall()

    durata = 0
    for da, a in lista_piogge:
        da = util.timestamp2datetime(da)
        da = da if da >= dal - DT else dal - DT

        a = util.timestamp2datetime(a)
        a = a if a <= al else al
        durata += (a - da).seconds / 60

    return durata


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
