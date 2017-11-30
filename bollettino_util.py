# 29.11.17 rev0
import calendar
import statistics
from pprint import pprint as pp

import db
import util
import vento_util
from costanti import *


class Bollettino(object):
    def __init__(self, anno, mese):
        self.anno = anno
        self.mese = mese

        self.db = db.DB()
        self.ngiorni = calendar.monthrange(anno, mese)[1]
        self.dal = datetime.datetime(anno, mese, 1)

        # self.crea_tabella_crea()

    def crea_tabella_crea(self):
        cur = self.db.cur
        db = self.db.db

        # tabella 1
        tabella1 = []
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
            data = [util.timestamp2date(h8[0]), ]
            pres = [h8[1], h14[1], h19[1]]
            t = [h8[2], None, None, h14[2], None, None, h19[2], None, None]
            ur = [h8[3], h14[3], h19[3], statistics.mean((h8[3], h14[3], h19[3])), None]
            t_min_tmax_tmedia = [tmmm[1], tmmm[2], (tmmm[1] + tmmm[2] + h8[2] + h19[2]) / 4.0]
            mm_8_14_19 = pioggia[1:]

            rec = []
            for campo in (data, pres, t, ur, t_min_tmax_tmedia, mm_8_14_19, neve):
                rec.extend(campo)

            tabella1.append(rec)

        # tabella 2
        tabella2 = []
        cmd_vd_vv = """
                SELECT data, vdir, vvel
                FROM Raw
                WHERE data
                BETWEEN '{dal}' AND datetime('{dal}', '+1 months')
                AND (strftime('%H:%M', data) = '08:00' OR
                     strftime('%H:%M', data) = '14:00' OR
                     strftime('%H:%M', data) = '19:00')
                """.format(dal=self.dal)
        dati_vd_vv = cur.execute(cmd_vd_vv).fetchall()

        ore8 = [(x[0], vento_util.direzione_vento(x[1], x[2]))
                for x in dati_vd_vv[slice(0, len(dati_vd_vv), 3)]]
        ore14 = [(x[0], vento_util.direzione_vento(x[1], x[2]))
                 for x in dati_vd_vv[slice(1, len(dati_vd_vv), 3)]]
        ore19 = [(x[0], vento_util.direzione_vento(x[1], x[2]))
                 for x in dati_vd_vv[slice(2, len(dati_vd_vv), 3)]]

        vento = self.calcola_vento_per_crea()

        eliof_rad = self.calcola_eliofania_radiazione_per_crea()

        ###############
        for h8, h14, h19, v, e_r in zip(ore8, ore14, ore19, vento, eliof_rad):
            data = [util.timestamp2date(h8[0]), ]
            v_d_v = [h8[1][0], h8[1][1], h14[1][0], h14[1][1], h19[1][0], h19[1][1]]
            v_km_max = v[1:]
            cielo = [None] * 8
            e_r = e_r[1:]
            suolo = [None] * 2

            rec = []
            for campo in (data, v_d_v, v_km_max, cielo, e_r, suolo):
                rec.extend(campo)

            tabella2.append(rec)

        # inserimento dati
        self.db.crea_tabelle_bollettino_crea()

        ncampi = len(tabella1[0])
        campi = ', '.join(['?'] * ncampi)
        cur.executemany('INSERT INTO Bollettino1 VALUES ({campi})'.format(campi=campi),
                        tabella1)

        ncampi = len(tabella2[0])
        campi = ', '.join(['?'] * ncampi)
        cur.executemany('INSERT INTO Bollettino2 VALUES ({campi})'.format(campi=campi),
                        tabella2)
        db.commit()

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
            durata = datetime.time(ore, minuti).strftime(TIME_SHORT_PF)

            # todo: max pioggia in un'ora calcolata prendendo dalla tabella oraria il max
            cmd = """
                    SELECT data, max(mm) 
                    FROM Orario
                    WHERE data
                    BETWEEN datetime('{giorno}', 'start of day', '-4 hours') AND 
                            datetime('{giorno}', 'start of day', '+19 hours') 
                    """.format(giorno=day)
            dati = cur.execute(cmd).fetchall()[0]
            ora_max, mm_max = (util.timestamp2time(dati[0]).hour, dati[1]) if dati[1] else (None, None)

            rec = [dati_mm8[0],
                   dati_mm8[1],
                   dati_mm14[0],
                   dati_mm19[0],
                   totale,
                   durata,
                   mm_max,
                   ora_max,
                   ]

            mm.append(rec)

        return mm

    def calcola_vento_per_crea(self):
        cur = self.db.cur
        anno = self.anno
        mese = self.mese

        ngiorni = self.ngiorni

        vento = []
        for giorno in range(1, ngiorni + 1):
            day = datetime.datetime(anno, mese, giorno)
            cmd = """
            SELECT vvel, data
            FROM Raw
            WHERE data BETWEEN datetime('{giorno}', 'start of day', '-1 days','+19 hours', '+10 minutes') AND 
                               datetime('{giorno}', 'start of day', '+19 hours')
            AND vvel IS NOT NULL 
            """.format(giorno=day)

            dati = cur.execute(cmd).fetchall()

            v = ([x[0] for x in dati])
            km_tot = sum(v) * 0.6  # 1[m/s] * 10 [minuti] = 0.6 [km]

            # todo: km_media da capire cosa si intende
            km_media = statistics.mean(v) * 0.6  # media km all'ora
            vmax, ora = max(dati)

            ora = util.timestamp2time(ora)
            ora = ora.hour + 1 if ora.minute else ora.hour

            rec = (day, km_tot, km_media, vmax, ora)
            vento.append(rec)

        return vento

    def calcola_eliofania_radiazione_per_crea(self):
        cur = self.db.cur
        anno = self.anno
        mese = self.mese

        ngiorni = self.ngiorni

        e_r = []
        for giorno in range(1, ngiorni + 1):
            day = datetime.datetime(anno, mese, giorno)
            cmd = """
            SELECT DATE(data), sum(eliof), sum(pir)
            FROM Raw
            WHERE data BETWEEN datetime('{giorno}', 'start of day', '-1 days','+20 hours') AND 
                               datetime('{giorno}', 'start of day', '+19 hours')
            """.format(giorno=day)

            dati = cur.execute(cmd).fetchone()

            e_r.append(dati)

        return e_r

    def xls_crea(self):
        cur = self.db.cur

        xls = []
        cmd1 = """
        SELECT *
        FROM Bollettino1
        WHERE strftime('%d', data) BETWEEN '01' AND '10'
        """
        cmd2 = """
        SELECT *
        FROM Bollettino2
        WHERE strftime('%d', data) BETWEEN '01' AND '10'
        """

        res1 = self.db.cur.execute(cmd1).fetchall()
        res2 = self.db.cur.execute(cmd2).fetchall()

        for rec in res1:
            rec = [x if x != None else '' for x in rec]
            formati = ('%s',  # data
                       '%.1f', '%.1f', '%.1f',  # pressione
                       '%.1f', '%s', '%s', '%.1f', '%s', '%s', '%.1f', '%s', '%s',  # temperatura
                       '%.0f', '%.0f', '%.0f',  # umidità
                       '%.1f', '%s', '%.1f', '%.1f', '%.1f',  # umidità media... temperatura media
                       '%.1f', '%.1f', '%.1f', '%.1f', '%s;', '%s', '%s',  # pioggia
                       '%s', '%s'  # neve
                       )
            rigo = ';'.join(formati) % tuple(rec)
            xls.append(rigo)

        xls.extend([''] * 3)

        for rec in res2:
            rec = [x if x != None else '' for x in rec]
            formati = ('%s',  # data
                       '%s', '%.1f', '%s', '%.1f', '%s', '%.1f', '%.1f', '%.1f', '%.1f', '%i',  # vento
                       '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',  # cielo
                       '%.1f', '%.1f',  # eliofania, radiazione
                       '%s', '%s'  # suolo
                       )
            rigo = ';'.join(formati) % tuple(rec)
            xls.append(rigo)

        xls.extend([''] * 3)

        with open(FOUT_CREA % (self.anno, self.mese), 'w') as fout:
            xls = '\n'.join(xls).replace('.', ',')

            fout.write(xls)
