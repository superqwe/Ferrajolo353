# 27.07.18
import calendar
import sqlite3 as lite

import pandas as pd
from matplotlib.cbook import boxplot_stats

from costanti import *


class annuario_talsano(object):
    """
    annuario dal 1975 al 2006
    :return:
    """

    def __init__(self):
        self._dati_grafici()

    def latex_dati_giornalieri(self, mese, anno):
        dati = self.mese(mese, anno)

        d1 = self._decade(dati, 1)
        d2 = self._decade(dati, 2)
        d3 = self._decade(dati, 3)

        ltx = TABELLA_DATI_GIORNALIERI % ({'mese': MESE[mese],
                                           'anno': anno,
                                           'decade1': d1,
                                           'decade2': d2,
                                           'decade3': d3,
                                           })

        return ltx

    def mese(self, mese, anno):
        dal = datetime.date(anno, mese, 1)
        al = datetime.date(anno, mese, calendar.monthrange(anno, mese)[1])

        cmd = '''SELECT data, tmed, tmin, tmax, press, ur, tens, mm, durata, nuvol, vvel, vdir, vfil
                 FROM Annuario_Talsano_G
                 WHERE data
                 BETWEEN '{dal}' AND '{al}'
                 '''.format(dal=dal,
                            al=al)
        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            dati = cur.execute(cmd).fetchall()

            return (dati)

    def _decade(self, dati, decade):
        da = 10 * (decade - 1)
        a = da + 10

        if decade == 3:
            a = None

        righe = []
        for d in dati[da:a]:
            # todo estrarre dal db tesc
            data, tmed, tmin, tmax, press, ur, tens, mm, durata, nuvol, vvel, vdir, vfil = d

            data = str(int(data[-2:]))

            # todo estrarre dal db
            try:
                tesc = tmax - tmin
            except TypeError:
                tesc = 0

            # formattazione righe
            # todo utilizzare _formatta_righe_dati
            tmin = '%.1f' % tmin if tmin != None else '-'
            tmax = '%.1f' % tmax if tmax != None else '-'
            tmed = '%.1f' % tmed if tmed != None else '-'
            tesc = '%.1f' % tesc if tesc else '-'
            press = '%.1f' % press if press else '-'
            ur = '%.1f' % ur if ur else '-'
            tens = '%.1f' % tens if tens else '-'
            mm = '%.1f' % mm if mm else ''
            durata = '%i' % durata if durata else ''
            nuvol = '%.1f' % nuvol if not nuvol == None else '-'
            vvel = '%.1f' % vvel if vvel else '-'
            vdir = '%s' % vdir if vdir else '-'
            vfil = '%i' % vfil if vfil else '-'

            rec = ' & '.join(
                (data, tmin, tmax, tmed, tesc, press, ur, tens, mm, durata, nuvol, vvel, vdir, vfil))
            rec += '\\\\\n'

            righe.append(rec)

        righe = ''.join(righe)

        return righe

    def _formatta_righe_dati(self, row, grandezza='anno'):
        data, tmed, tmin, tmax, tesc, press, ur, tens, mm, durata, nuvol, vvel, vdir, vfil = row

        if grandezza == 'anno':
            data = '%s' % data
        if grandezza == 'mese':
            data = data.split('-')[1]
        if grandezza == 'giorno':
            pass

        # formattazione righe
        tmin = '%.1f' % tmin if tmin is not None else '-'
        tmax = '%.1f' % tmax if tmax else '-'
        tmed = '%.1f' % tmed if tmed else '-'
        tesc = '%.1f' % tesc if tesc else '-'
        press = '%.1f' % press if press else '-'
        ur = '%.1f' % ur if ur else '-'
        tens = '%.1f' % tens if tens else '-'
        mm = '%.1f' % mm if mm is not None else ''
        durata = '%i' % durata if durata is not None else ''
        nuvol = '%.1f' % nuvol if nuvol else '-'
        vvel = '%.1f' % vvel if vvel else '-'
        vdir = '%s' % vdir if vdir else '-'
        vfil = '%i' % vfil if vfil else '-'

        rec = ' & '.join(
            (data, tmin, tmax, tmed, tesc, press, ur, tens, mm, durata, nuvol, vvel, vdir, vfil))
        rec += '\\\\\n'

        return rec

    def latex_dati_mensili(self, anno):
        dati1 = self.dati_mensili(anno)
        dati2 = self.dati_mensili(anno + 1)

        righe1 = []
        righe2 = []

        for row in (dati1.values):
            rec = self._formatta_righe_dati(row, 'mese')
            righe1.append(rec)

        for row in (dati2.values):
            rec = self._formatta_righe_dati(row, 'mese')
            righe2.append(rec)

        righe1 = ''.join(righe1)
        righe2 = ''.join(righe2)

        # todo sistemare i dati nan in fase di richiesta dati
        righe1 = righe1.replace('nan', '-')
        righe2 = righe2.replace('nan', '-')

        ltx = TABELLA_DATI_MENSILI % ({'anno1': anno, 'mensile1': righe1,
                                       'anno2': anno + 1, 'mensile2': righe2})

        return ltx

    def dati_mensili(self, anno):
        dal = datetime.date(anno, 1, 1)
        al = datetime.date(anno, 12, 31)

        cmd = '''SELECT *
                 FROM Annuario_Talsano_M
                 WHERE data
                 BETWEEN '{dal}' AND '{al}'
                 '''.format(dal=dal,
                            al=al)

        with lite.connect(NOME_DB) as con:
            dati = pd.read_sql(cmd, con)

            return (dati)

    def latex_dati_anni(self):
        dati = self.dati_annuali()

        righe = []
        for row in (dati.values):
            rec = self._formatta_righe_dati(row, 'anno')

            righe.append(rec)

        righe = ''.join(righe)

        # todo sistemare i dati nan in fase di richiesta dati
        righe = righe.replace('nan', '-')

        ltx = TABELLA_DATI_ANNUALI % ({'annuali': righe, })

        return ltx

    def dati_annuali(self):
        cmd = '''SELECT *
                 FROM Annuario_Talsano_A
                 '''

        with lite.connect(NOME_DB) as con:
            dati = pd.read_sql(cmd, con)

            return (dati)

    def _dati_grafici(self):
        # todo aggiungere scarto
        # temperatura
        self.t_mese = self._t_mese()
        self.t_anno = self._t_anno()

        # pioggia
        self.p_anno = self._p_anno()
        self.p_mese = self._p_mese()

        self.pg_anno = self._pg_anno()
        self.pg_mese = self._pg_mese()

        self.pf_anno = self._pf_anno()

        # self._frequenza_giorni_piovosi()

    def _t_mese(self):
        dal = datetime.date(1975, 1, 1)
        al = datetime.date(2006, 12, 31)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()

            parametri = {0: 'tmax', 1: 'tmed', 2: 'tmin'}
            dati = [[], [], []]
            for par in range(3):

                for mese in range(1, 12 + 1):
                    mese = '%02i' % mese
                    cmd = '''SELECT {parametro}
                             FROM Annuario_Talsano_G
                             WHERE {parametro} IS NOT NULL 
                             AND strftime('%m', data)=='{mese}'
                             AND data BETWEEN '{dal}' AND '{al}'
                          '''.format(dal=dal, al=al, mese=mese, parametro=parametri[par])

                    res = cur.execute(cmd).fetchall()
                    res = [x[0] for x in res]
                    dati[par].append(res)

        return dati

    def _t_anno(self):

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()

            parametri = {0: 'tmax', 1: 'tmed', 2: 'tmin'}
            dati = [[], [], []]
            for par in range(3):

                for anno in range(1975, 2006 + 1):
                    dal = datetime.date(anno, 1, 1)
                    al = datetime.date(anno, 12, 31)

                    cmd = '''SELECT {parametro}
                                 FROM Annuario_Talsano_G
                                 WHERE {parametro} IS NOT NULL 
                                 AND data BETWEEN '{dal}' AND '{al}'
                              '''.format(dal=dal, al=al, parametro=parametri[par])

                    res = cur.execute(cmd).fetchall()
                    res = ([x[0] for x in res])
                    dati[par].append(res)

        return dati

    def _p_anno(self):
        mm = []
        parametro = 'mm'
        with lite.connect(NOME_DB) as con:
            cur = con.cursor()

            for anno in range(1975, 2006 + 1):
                dal = datetime.date(anno, 1, 1)
                al = datetime.date(anno, 12, 31)

                cmd = '''SELECT {parametro}
                             FROM Annuario_Talsano_G
                             WHERE {parametro} IS NOT NULL 
                             AND data BETWEEN '{dal}' AND '{al}'
                          '''.format(dal=dal, al=al, parametro=parametro)

                res = cur.execute(cmd).fetchall()
                res = sum([x[0] for x in res])

                mm.append(res)
        stat = boxplot_stats(mm)
        return mm, stat

    def _p_mese(self):
        parametro = 'mm'
        dal = datetime.date(1975, 1, 1)
        al = datetime.date(2006, 12, 31)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            mm = []

            for mese in range(1, 12 + 1):
                mese = '%02i' % mese
                cmd = '''SELECT {parametro}
                         FROM Annuario_Talsano_M
                         WHERE {parametro} IS NOT NULL 
                         AND strftime('%m', data)=='{mese}'
                         AND data BETWEEN '{dal}' AND '{al}'
                      '''.format(dal=dal, al=al, mese=mese, parametro=parametro)

                dati = cur.execute(cmd).fetchall()
                mm.append([x[0] for x in dati])

        # stat = boxplot_stats(mm)
        return mm

    def _pg_anno(self):
        mm = []
        parametro = 'mm'
        with lite.connect(NOME_DB) as con:
            cur = con.cursor()

            for anno in range(1975, 2006 + 1):
                dal = datetime.date(anno, 1, 1)
                al = datetime.date(anno, 12, 31)

                cmd = '''SELECT count({parametro})
                             FROM Annuario_Talsano_G
                             WHERE {parametro} > 0 
                             AND data BETWEEN '{dal}' AND '{al}'
                          '''.format(dal=dal, al=al, parametro=parametro)

                res = cur.execute(cmd).fetchall()[0][0]
                mm.append(res)

        stat = boxplot_stats(mm)
        return mm, stat

    def _pg_mese(self):
        parametro = 'mm'
        dal = datetime.date(1975, 1, 1)
        al = datetime.date(2006, 12, 31)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            gp = {'%02i' % x: [] for x in range(1, 13)}

            for anno in range(1975, 2006 + 1):
                for mese in range(1, 12 + 1):
                    gg = calendar.monthrange(anno, mese)[1]
                    dal = datetime.date(anno, mese, 1)
                    al = datetime.date(anno, mese, gg)

                    mese = '%02i' % mese

                    cmd = '''SELECT count({parametro})
                             FROM Annuario_Talsano_G
                             WHERE {parametro} > 0 
                             AND strftime('%m', data)=='{mese}'
                             AND data BETWEEN '{dal}' AND '{al}'
                          '''.format(dal=dal, al=al, mese=mese, parametro=parametro)

                    dati = cur.execute(cmd).fetchall()[0][0]
                    gp[mese].append(dati)

        # stat = boxplot_stats(mm)

        # trasforma gp da dizionario in lista di liste ordinata per mesi
        gp_ordinati = [gp[x] for x in sorted(gp.keys())]

        return gp_ordinati

    def _pf_anno(self):
        mm = []
        parametro = 'mm'
        with lite.connect(NOME_DB) as con:
            cur = con.cursor()

            dal = datetime.date(1975, 1, 1)
            al = datetime.date(2006, 12, 31)

            cmd = '''SELECT {parametro}
                                FROM Annuario_Talsano_G
                                WHERE {parametro} > 0 
                                AND data BETWEEN '{dal}' AND '{al}'
                             '''.format(dal=dal, al=al, parametro=parametro)

            res = cur.execute(cmd).fetchall()
            mm.append([x[0] for x in res])

        return mm
