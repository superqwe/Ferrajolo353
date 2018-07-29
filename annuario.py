# 27.07.18
import calendar
import sqlite3 as lite
from pprint import pprint as pp

from costanti import *


class annuario_talsano(object):
    """
    annuario dal 1975 al 2006
    :return:
    """

    def __init__(self):
        pass

    def mese(self, mese, anno):
        dal = datetime.date(anno, mese, 1)
        al = datetime.date(anno, mese, calendar.monthrange(anno, mese)[1])

        cmd = '''SELECT data, t, tmin, tmax, pres, mm, durata, ur
                 FROM Giornaliero
                 WHERE data
                 BETWEEN '{dal}' AND '{al}'
                 '''.format(dal=dal,
                            al=al)
        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            dati = cur.execute(cmd).fetchall()

            return (dati)

    def latex_mese(self, mese, anno):
        dati = self.mese(mese, anno)

        data = datetime.date(anno, mese, 1)

        d1 = self._decade(dati, 1)
        d2 = self._decade(dati, 2)
        d3 = self._decade(dati, 3)

        cmd = '''SELECT t, tmin, tmax, pres, ur, mm, durata
                 FROM Mensile
                 WHERE data = '{data}'
              '''.format(data=data)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            a = cur.execute(cmd).fetchall()[0]
            tmed, tmin, tmax, press, ur, mm, durata = a

            # print(a)

            # todo correggere assenzza valori
            press = 0
            ur = '%.1f' % ur if ur else '-'

        try:
            mensile = ' & '.join(('%.1f' % tmin, '%.1f' % tmax, '%.1f' % tmed, '%.1f' % (tmax - tmin),
                                  '%.1f' % press, '%.1f' % ur, '%.1f' % mm, '%i' % durata))
        except TypeError:
            mensile = ' & '.join(('-', '-', '-', '-', '-', '-', '-', '-'))

        ltx = TABELLA_MESE % ({'mese': MESE[mese],
                               'anno': anno,
                               'decade1': d1[0],
                               'decade2': d2[0],
                               'decade3': d3[0],
                               'med_decade1': d1[1],
                               'med_decade2': d2[1],
                               'med_decade3': d3[1],
                               'mensile': mensile
                               })

        return ltx

    def _decade(self, dati, decade):
        da = 10 * (decade - 1)
        a = da + 10

        if decade == 3:
            a = None

        righe = []
        dtmed = 0
        dtmin = 100
        dtmax = -100
        dtesc = 0
        dpress = 0
        dmm = 0
        ddurata = 0
        dur = 0
        for d in dati[da:a]:
            data, tmed, tmin, tmax, press, mm, durata, ur = d

            # print(d)

            data = str(int(data[-2:]))

            try:
                tesc = tmax - tmin
            except TypeError:
                tesc = 0

            dtmed += tmed if tmed else 0

            if tmin:
                dtmin = tmin if tmin < dtmin else dtmin

            if tmax:
                dtmax = tmax if tmax > dtmax else dtmax

            try:
                dtesc += tmax - tmin
            except TypeError:
                pass

            dpress += 0  # todo correggere assenza valori
            dmm += mm if mm else 0  # todo corregere assenza valori
            ddurata += durata if durata else 0  # todo corregere assenza valori
            dur += ur if ur else 0  # todo corregere assenza valori

            if press:
                press = str(press)
            else:
                press = ''

            rec = ' & '.join((data, str(tmin), str(tmax), str(tmed), '%.1f' % tesc, press, str(ur), str(mm),
                              str(durata)))
            rec += '\\\\\n'

            righe.append(rec)

        righe = ''.join(righe)

        n = len(dati[da:a])
        dtmed /= n
        dtesc /= n
        dpress /= n
        dur /= n

        decadale = ' & '.join(
            ('%.1f' % dtmin, '%.1f' % dtmax, '%.1f' % dtmed, '%.1f' % dtesc, '%.1f' % dpress,
             '%.1f' % dur, '%.1f' % dmm, '%i' % ddurata))

        return righe, decadale
