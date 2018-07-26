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

        # tabella 1
        d1 = self._decade(dati, 1, 1)
        d2 = self._decade(dati, 2, 1)
        d3 = self._decade(dati, 3, 1)

        cmd = '''SELECT t, tmin, tmax, pres, mm, durata
                 FROM Mensile
                 WHERE data = '{data}'
              '''.format(data=data)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            a = cur.execute(cmd).fetchall()[0]
            tmed, tmin, tmax, press, mm, durata = a

            # print(a)

            # todo correggere assenzza valori
            press = 0

        try:
            mensile = ' & '.join(('%.1f' % tmin, '%.1f' % tmax, '%.1f' % tmed, '%.1f' % (tmax - tmin),
                                  '%.1f' % press))
        except TypeError:
            mensile = ' & '.join(('-', '-', '-', '-', '-'))

        ltx1 = TABELLA_MESE_1 % ({'mese': MESE[mese],
                                  'anno': anno,
                                  'decade1': d1[0],
                                  'decade2': d2[0],
                                  'decade3': d3[0],
                                  'med_decade1': d1[1],
                                  'med_decade2': d2[1],
                                  'med_decade3': d3[1],
                                  'mensile': mensile
                                  })

        # tabella 2
        d1 = self._decade(dati, 1, 2)
        d2 = self._decade(dati, 2, 2)
        d3 = self._decade(dati, 3, 2)

        cmd = '''SELECT mm, durata, ur
                 FROM Mensile
                 WHERE data = '{data}'
              '''.format(data=data)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            mm, durata, ur = cur.execute(cmd).fetchall()[0]

        # print(mm, durata, ur)
        ur = '%.1f' % ur if ur else '-'

        try:
            mensile = ' & '.join(('%.1f' % mm, '%i' % durata, ur,))
        except TypeError:
            mensile = ' & '.join(('-', '-', '-'))

        ltx2 = TABELLA_MESE_2 % ({'mese': MESE[mese],
                                  'anno': anno,
                                  'decade1': d1[0],
                                  'decade2': d2[0],
                                  'decade3': d3[0],
                                  'med_decade1': d1[1],
                                  'med_decade2': d2[1],
                                  'med_decade3': d3[1],
                                  'mensile': mensile
                                  })

        return ltx1 + ltx2

    def _decade(self, dati, decade, tabella):
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

            if tabella == 1:
                rec = ' & '.join((data, str(tmin), str(tmax), str(tmed), '%.1f' % tesc, press, '\\\\\n'))
            else:
                rec = ' & '.join((data, str(mm), str(durata), str(ur), '\\\\\n'))

            righe.append(rec)

        righe = ''.join(righe)

        n = len(dati[da:a])
        dtmed /= n
        dtesc /= n
        dpress /= n
        dur /= n

        if tabella == 1:
            decadale = ' & '.join(
                ('%.1f' % dtmin, '%.1f' % dtmax, '%.1f' % dtmed, '%.1f' % dtesc, '%.1f' % dpress))
        else:
            decadale = ' & '.join(
                ('%.1f' % dmm, '%i' % ddurata, '%.1f' % dur))

        return righe, decadale
