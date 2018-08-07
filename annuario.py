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
        self._dati_grafici()

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

            dpress += press if press else 0  # todo correggere assenza valori
            dmm += mm if mm else 0  # todo corregere assenza valori
            ddurata += durata if durata else 0  # todo corregere assenza valori
            dur += ur if ur else 0  # todo corregere assenza valori

            # formattazione righe
            tmin = '%.1f' % tmin if tmin else '-'
            tmax = '%.1f' % tmax if tmax else '-'
            tmed = '%.1f' % tmed if tmed else '-'
            tesc = '%.1f' % tesc if tesc else '-'
            press = '%.1f' % press if press else '-'
            ur = '%.1f' % ur if ur else '-'
            mm = '%.1f' % mm if mm else ''
            durata = '%i' % durata if durata else ''

            rec = ' & '.join((data, tmin, tmax, tmed, tesc, press, ur, mm, durata))
            rec += '\\\\\n'

            righe.append(rec)

        righe = ''.join(righe)

        n = len(dati[da:a])
        dtmed /= n
        dtesc /= n
        dpress /= n
        dur /= n

        # formattazione rigo decadale
        dpress = '%.1f' % dpress if dpress else '-'
        dur = '%.1f' % dur if dur else '-'

        decadale = ' & '.join(
            ('%.1f' % dtmin, '%.1f' % dtmax, '%.1f' % dtmed, '%.1f' % dtesc, dpress, dur, '%.1f' % dmm,
             '%i' % ddurata))

        return righe, decadale

    def _dati_grafici(self):
        # temperatura
        self.tmin_mese = self._t_min_mese()
        self.tmax_mese = self._t_max_mese()
        self.tmed_mese = self._t_med_mese()

        # self.tmin_anno = self._t_min_anno()
        # self.tmax_anno = self._t_max_anno()
        # self.tmed_anno = self._t_med_anno()

        # pioggia
        # self._media_mensile()
        # self._cumulata_mese()
        # self._n_giorni_piovosi()
        # self._frequenza_giorni_piovosi()

    def _t_min_mese(self):
        dal = datetime.date(1975, 1, 1)
        al = datetime.date(2006, 12, 31)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            tmin = []

            for mese in range(1, 12 + 1):
                mese = '%02i' % mese
                cmd = '''SELECT tmin
                         FROM Giornaliero
                         WHERE tmin IS NOT NULL 
                         AND strftime('%m', data)=='{mese}'
                         AND data BETWEEN '{dal}' AND '{al}'
                      '''.format(dal=dal, al=al, mese=mese)

                dati = cur.execute(cmd).fetchall()
                tmin.append([x[0] for x in dati])

        return tmin

    def _t_max_mese(self):
        dal = datetime.date(1975, 1, 1)
        al = datetime.date(2006, 12, 31)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            tmax = []

            for mese in range(1, 12 + 1):
                mese = '%02i' % mese
                cmd = '''SELECT tmax
                         FROM Giornaliero
                         WHERE tmin IS NOT NULL 
                         AND strftime('%m', data)=='{mese}'
                         AND data BETWEEN '{dal}' AND '{al}'
                      '''.format(dal=dal, al=al, mese=mese)

                dati = cur.execute(cmd).fetchall()
                tmax.append([x[0] for x in dati])

        return tmax

    def _t_med_mese(self):
        dal = datetime.date(1975, 1, 1)
        al = datetime.date(2006, 12, 31)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            tmed = []

            for mese in range(1, 12 + 1):
                mese = '%02i' % mese
                cmd = '''SELECT t
                         FROM Giornaliero
                         WHERE tmin IS NOT NULL 
                         AND strftime('%m', data)=='{mese}'
                         AND data BETWEEN '{dal}' AND '{al}'
                      '''.format(dal=dal, al=al, mese=mese)

                dati = cur.execute(cmd).fetchall()
                tmed.append([x[0] for x in dati])

        return tmed
