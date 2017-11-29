# 29.11.17 rev0
import calendar
import sqlite3 as lite

from costanti import *


class Bollettino(object):
    def __init__(self, anno, mese):
        self.anno = anno
        self.mese = mese
        self.ngiorni = calendar.monthrange(anno, mese)[1]
        self.dal = datetime.datetime(anno, mese, 1)

        self.analizza_per_tabella_creaa()

    def analizza_per_tabella_creaa(self):

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()

            cmd_pres_t_ur = """
            SELECT data, pres, t, ur
            FROM Raw
            WHERE data
            BETWEEN '{dal}' AND datetime('{dal}', '+1 months')
            AND (strftime('%H:%M', data) = '08:00' OR
                 strftime('%H:%M', data) = '14:00' OR
                 strftime('%H:%M', data) = '19:00')
            """.format(dal=self.dal)
            dati_pres_t_ur = cur.execute(cmd_pres_t_ur).fetchall()

            ore8 = [x for x in dati_pres_t_ur[slice(0, len(dati_pres_t_ur), 3)]]
            ore14 = [x for x in dati_pres_t_ur[slice(1, len(dati_pres_t_ur), 3)]]
            ore19 = [x for x in dati_pres_t_ur[slice(2, len(dati_pres_t_ur), 3)]]

            cmd_tmin_tmax = """
            SELECT data, tmin, tmax
            FROM Giornaliero
            WHERE data
            BETWEEN date('{dal}') AND date('{dal}', '+1 months', '-1 days')
            """.format(dal=self.dal)
            dati_tmin_tmax = cur.execute(cmd_tmin_tmax).fetchall()

            mm = self.calcola_pioggia_per_crea(cur)

            neve = [None, None]

            ##################
            for h8, h14, h19, tmmm, pioggia in zip(ore8, ore14, ore19, dati_tmin_tmax, mm):
                pres = [h8[1], h14[1], h19[1]]
                t = [h8[2], None, None, h14[2], None, None, h19[2], None, None]
                ur = [h8[3], h14[3], h19[3], statistics.mean((h8[3], h14[3], h19[3])), None]
                t_min_tmax_tmedia = [tmmm[1], tmmm[2], (tmmm[1] + tmmm[2] + h8[2] + h19[2]) / 4.0]
                mm_8_14_19 = pioggia[1:]

                rec = []
                for campo in (pres, t, ur, t_min_tmax_tmedia, mm_8_14_19, neve):
                    rec.extend(campo)

                print(rec)

    def calcola_pioggia_per_crea(self, cur):
        anno = self.anno
        mese = self.mese
        ngiorni = calendar.monthrange(anno, mese)[1]

        mm = []
        for giorno in range(1, ngiorni + 1):
            day = datetime.datetime(anno, mese, giorno)
            cmd_mm8 = """
                        SELECT date(data), sum(mm), sum(durata)
                        FROM Orario
                        WHERE data
                        BETWEEN datetime('{giorno}', 'start of day', '-4 hours') AND 
                                datetime('{giorno}', 'start of day', '+8 hours') 
                        """.format(giorno=day)
            dati_mm8 = cur.execute(cmd_mm8).fetchall()[0]

            cmd_mm14 = """
                        SELECT sum(mm), sum(durata)
                        FROM Orario
                        WHERE data
                        BETWEEN datetime('{giorno}', 'start of day', '+9 hours') AND 
                                datetime('{giorno}', 'start of day', '+14 hours') 
                        """.format(giorno=day)
            dati_mm14 = cur.execute(cmd_mm14).fetchall()[0]

            cmd_mm19 = """
                        SELECT sum(mm), sum(durata)
                        FROM Orario
                        WHERE data
                        BETWEEN datetime('{giorno}', 'start of day', '+15 hours') AND 
                                datetime('{giorno}', 'start of day', '+19 hours') 
                        """.format(giorno=day)
            dati_mm19 = cur.execute(cmd_mm19).fetchall()[0]

            totale = sum((dati_mm8[1], dati_mm14[0], dati_mm19[0]))

            durata = sum((dati_mm8[2], dati_mm14[1], dati_mm19[1]))
            ore, minuti = util.minuti2ore_minuti(durata)

            # todo: max pioggia in un'ora calcolata prendendo dalla tabella oraria il max
            cmd = """
                    SELECT data, max(mm) 
                    FROM Orario
                    WHERE data
                    BETWEEN datetime('{giorno}', 'start of day', '-4 hours') AND 
                            datetime('{giorno}', 'start of day', '+19 hours') 
                    """.format(giorno=day)
            dati = cur.execute(cmd).fetchall()[0]
            ora_max, mm_max = dati if dati[1] else ('', 0)

            rec = [dati_mm8[0],
                   dati_mm8[1],
                   dati_mm14[0],
                   dati_mm19[0],
                   totale,
                   ore,
                   minuti,
                   ora_max,
                   mm_max,
                   ]

            mm.append(rec)

        return mm
