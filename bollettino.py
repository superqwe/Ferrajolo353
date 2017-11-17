# 09.11.17: rev0

import calendar
import csv
import datetime
import statistics

from pprint import pprint as pp

import eliofania
import pdf

# se tra un dato di pioggia rilevato ed un altro non supera questo tempo, allora la pioggia è continua
DT_PIOGGIA = datetime.timedelta(minutes=30)
# nome file di output
FOUT_DECADALE = 'decadale.csv'
FOUT_MENSILE_CSV = 'mensile.csv'
FOUT_PIOGGIA_CSV = 'pioggia.csv'


class Bollettino(object):
    def __init__(self, mese):
        self.mese = int(mese[2:])
        self.anno = 2000 + int(mese[:2])
        self.__fin = '%sm.txt' % mese
        self.__leggi_csv()

        self.__analizza_per_bollettino_decadale()
        self.__bollettino_decadale()

        self.__analizza_per_bollettino_mensile()
        self.__bollettino_mensile_csv()
        self.__bollettino_mensile_pdf()

        self.__analizza_per_bollettino_pioggia()
        self.__bollettino_pioggia()
        self.__bollettino_pioggia_pdf()

    def __leggi_csv(self):
        with open(self.__fin) as f:
            reader = csv.DictReader(f, delimiter=';')
            dati = []

            self.__dati = {}
            for row in reader:
                giorno = row['GIORNO']
                ora = '23.59' if row['ORA'] == '24.00' else row['ORA']

                data = '%s %s' % (giorno, ora)

                try:
                    data = datetime.datetime.strptime(data, '%d/%m/%Y %H.%M')

                    # correzione fuso orario italia
                    if ora == '23.59':
                        data += datetime.timedelta(minutes=61)
                    else:
                        data += datetime.timedelta(minutes=60)

                except ValueError:
                    print('dato mancante', row['GIORNO'], row['ORA'])

                t = row['TARANTO T Aria 2m (MED) °C'] if row['TARANTO T Aria 2m (MED) °C'] else None
                tmin = row['TARANTO T Aria 2m (MIN) °C'] if row['TARANTO T Aria 2m (MIN) °C'] else None
                tmax = row['TARANTO T Aria 2m (MAX) °C'] if row['TARANTO T Aria 2m (MAX) °C'] else None
                pres = row['TARANTO PR 2m (MED) hPa'] if row['TARANTO PR 2m (MED) hPa'] else None
                mm = float(row['TARANTO PLUV (MED) mm']) if row['TARANTO PLUV (MED) mm'] else None
                vvel = float(row['TARANTO VEL V 10m (MED) m/s']) if row[
                    'TARANTO VEL V 10m (MED) m/s'] else None
                vdir = row['TARANTO DIR V 10m (MED) GN'] if row['TARANTO DIR V 10m (MED) GN'] else None
                ur = row['TARANTO UM 2m (MED) %'] if row['TARANTO UM 2m (MED) %'] else None
                eliof = float(row['TARANTO ELIOF (MED) min']) if row['TARANTO ELIOF (MED) min'] else None
                pir = float(row['TARANTO PIR (MED) W/m2']) if row['TARANTO PIR (MED) W/m2'] else None

                self.__dati[data] = {
                    't': t, 'tmin': tmin, 'tmax': tmax,
                    'pres': pres, 'mm': mm, 'ur': ur,
                    'vvel': vvel, 'vdir': vdir,
                    'eliof': eliof, 'pir': pir}

    def __analizza_per_bollettino_decadale(self):
        anno = self.anno
        mese = self.mese
        # todo: ngiorni da calcolare
        ngiorni = 31

        bollettino = []
        for giorno in range(1, ngiorni + 1):
            # temperatura
            t8 = float(self.__dati[datetime.datetime(anno, mese, giorno, 8)]['t'])
            t14 = float(self.__dati[datetime.datetime(anno, mese, giorno, 14)]['t'])
            t19 = float(self.__dati[datetime.datetime(anno, mese, giorno, 19)]['t'])

            tmin = min([float(self.__dati[datetime.datetime(anno, mese, giorno, h)]['tmin'])
                        for h in range(24)
                        if datetime.datetime(anno, mese, giorno, h) in self.__dati])
            tmax = max([float(self.__dati[datetime.datetime(anno, mese, giorno, h)]['tmax'])
                        for h in range(24)
                        if datetime.datetime(anno, mese, giorno, h) in self.__dati])

            tmedia = (t8 + t19 + tmin + tmax) / 4

            # umidità
            ur8 = float(self.__dati[datetime.datetime(anno, mese, giorno, 8)]['ur'])
            ur14 = float(self.__dati[datetime.datetime(anno, mese, giorno, 14)]['ur'])
            ur19 = float(self.__dati[datetime.datetime(anno, mese, giorno, 19)]['ur'])
            ur_media = (ur8 + ur14 + ur19) / 3.0

            # pioggia
            mm8, mm14, mm19, mm, durata_ore, durata_minuti, mm_pioggia_max = self.__calcola_pioggia_bollettino_decadale(
                anno,
                mese,
                giorno)

            record1 = (
                '%.1f' % float(self.__dati[datetime.datetime(anno, mese, giorno, 8)]['pres']),
                '%.1f' % float(self.__dati[datetime.datetime(anno, mese, giorno, 14)]['pres']),
                '%.1f' % float(self.__dati[datetime.datetime(anno, mese, giorno, 19)]['pres']),
                '%.1f' % t8,
                '',
                '',
                '%.1f' % t14,
                '',
                '',
                '%.1f' % t19,
                '',
                '',
                '%.1f' % ur8,
                '%.1f' % ur14,
                '%.1f' % ur19,
                '%.2f' % ur_media,
                '',
                '%.1f' % tmin,
                '%.1f' % tmax,
                '%.1f' % tmedia,
                '%.1f' % mm8,
                '%.1f' % mm14,
                '%.1f' % mm19,
                '%.1f' % mm,
                '%.0f:%02.0f' % (durata_ore, durata_minuti),
                '',
                '%.1f' % mm_pioggia_max,
                '',
            )

            # vento
            vdir8, vvel8, vdir14, vvel14, vdir19, vvel19, km, velocita_media, velocita_max, orario = self.__calcola_vento_bollettino_decadale(
                anno, mese, giorno)

            #  todo: da chiarire se l'eliofania è dalle 19-19 o dalle 0-24 --- ora è 19-19
            # todo: chidere unità di misura dell'eliofania MINUTI od ORE --- ora è ORE
            dt = datetime.datetime(anno, mese, giorno, 0)
            dt19gp = dt - datetime.timedelta(hours=5)
            dt19 = datetime.datetime(anno, mese, giorno, 19)

            eliof = sum([self.__dati[dt]['eliof']
                         for dt in self.__dati
                         if dt19gp < dt <= dt19 and self.__dati[dt]['eliof']]) / 60

            # todo: da chiarire se l'eliofania è dalle 19-19 o dalle 0-24 --- ora è 19-19
            # 1 watt = 14.33075379765 cal/min
            # 1 m2 = 10000 cm2
            # 1 W/m2 = 00014.33075379765/10000 Cal/cm2/min = 0.001433075379765 Cal/cm2/min
            radiazione = sum([self.__dati[dt]['pir']
                              for dt in self.__dati
                              if dt19gp < dt <= dt19 and self.__dati[dt]['pir']]) * 0.001433075379765

            record2 = (
                vdir8,
                '%.1f' % vvel8,
                vdir14,
                '%.1f' % vvel14,
                vdir19,
                '%.1f' % vvel19,
                '%.1f' % km,
                '%.1f' % velocita_media,
                '%.1f' % velocita_max,
                orario,
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '%.3f' % eliof,
                '%.3f' % radiazione
            )

            bollettino.append((giorno, record1, record2))

            self.__dati_bollettino_decadale = bollettino

    def __calcola_vento_bollettino_decadale(self, anno, mese, giorno):
        vdir8 = self.__dati[datetime.datetime(anno, mese, giorno, 8)]['vdir']
        vvel8 = self.__dati[datetime.datetime(anno, mese, giorno, 8)]['vvel']
        vdir8, vvel8 = self.__direzione_vento(vdir8, vvel8)

        vdir14 = self.__dati[datetime.datetime(anno, mese, giorno, 14)]['vdir']
        vvel14 = self.__dati[datetime.datetime(anno, mese, giorno, 14)]['vvel']
        vdir14, vvel14 = self.__direzione_vento(vdir14, vvel14)

        vdir19 = self.__dati[datetime.datetime(anno, mese, giorno, 19)]['vdir']
        vvel19 = self.__dati[datetime.datetime(anno, mese, giorno, 19)]['vvel']
        vdir19, vvel19 = self.__direzione_vento(vdir19, vvel19)

        #  todo: da chiarire se i km percorsi sono da dalle 19-19 o dalle 0-24 --- ora è 19-19
        dt = datetime.datetime(anno, mese, giorno, 0)
        dt19gp = dt - datetime.timedelta(hours=5)
        dt19 = datetime.datetime(anno, mese, giorno, 19)

        velocita = [self.__dati[dt]['vvel']
                    for dt in self.__dati
                    if dt19gp < dt <= dt19]
        km = sum(velocita) * 3.6 / 6
        tempo = len([self.__dati[dt]['vvel']
                     for dt in self.__dati
                     if dt19gp < dt <= dt19 if self.__dati[dt]['vvel']]) / 6
        velocita_media = 0 if not tempo else sum(velocita) / tempo

        # todo: verificare se esiste il dato di velocità max
        velocita_max, orario = max([(self.__dati[dt]['vvel'], dt.strftime('%H:%M'))
                                    for dt in self.__dati
                                    if dt19gp < dt <= dt19])

        return vdir8, vvel8, vdir14, vvel14, vdir19, vvel19, km, velocita_media, velocita_max, orario

    def __direzione_vento(self, direzione, velocita):
        velocita = float(velocita)
        if velocita * 3.6 <= 5.0:
            return 'C', 0.0

        direzione = int(direzione)
        dg = 45 / 2
        if 45 - dg <= direzione < 45 + dg:
            direzione = 'NE'
        elif 90 - dg <= direzione < 90 + dg:
            direzione = 'E'
        elif 135 - dg <= direzione < 135 + dg:
            direzione = 'SE'
        elif 180 - dg <= direzione < 180 + dg:
            direzione = 'S'
        elif 225 - dg <= direzione < 225 + dg:
            direzione = 'SO'
        elif 270 - dg <= direzione < 270 + dg:
            direzione = 'O'
        elif 315 - dg <= direzione < 315 + dg:
            direzione = 'NO'
        else:
            direzione = 'N'

        return direzione, velocita

    def __calcola_pioggia_bollettino_decadale(self, anno, mese, giorno):
        dt = datetime.datetime(anno, mese, giorno, 0)
        dt19gp = dt - datetime.timedelta(hours=5)
        dt8 = datetime.datetime(anno, mese, giorno, 8)
        dt14 = datetime.datetime(anno, mese, giorno, 14)
        dt19 = datetime.datetime(anno, mese, giorno, 19)

        mm8 = sum([float(self.__dati[dt]['mm'])
                   for dt in self.__dati
                   if dt19gp < dt <= dt8 and float(self.__dati[dt]['mm'])])
        mm14 = sum([float(self.__dati[dt]['mm'])
                    for dt in self.__dati
                    if dt8 < dt <= dt14 and float(self.__dati[dt]['mm'])])
        mm19 = sum([float(self.__dati[dt]['mm'])
                    for dt in self.__dati
                    if dt14 < dt <= dt19 and float(self.__dati[dt]['mm'])])

        # todo: da chiarire cosa si intende per precipitazioni totale diurno --- ora è 19-19
        mm = mm8 + mm14 + mm19

        # todo: da chiarire se la durata della pioggia è dalle 19-19 o dalle 0-24  --- ora è 19-19
        # estrae i dati di pioggia del giorno
        durata = [rec
                  for rec in self.__dati
                  if dt19gp < rec <= dt19 and self.__dati[rec]['mm']]
        durata.sort()

        dt = datetime.timedelta(minutes=10)
        durata_ore = durata_minuti = 0
        if durata:
            # orari_piogge = [[dalle_1, alle_1], [dalle_2, alle_2], ...]
            orari_piogge = [[durata[0] - dt, durata[0]]]

            for rec in durata[1:]:

                if rec - DT_PIOGGIA > orari_piogge[-1][1]:
                    orari_piogge.append([rec - dt, rec])
                else:
                    orari_piogge[-1][1] = rec

            durata_totale = sum([(al - dal).seconds for dal, al in orari_piogge])
            durata_ore = durata_totale // (60 * 60)
            durata_minuti = (durata_totale % (60 * 60)) // 60

        # todo: da chiarire se la massima in un'ora à dalle 19-19 o dalle 0-24
        # todo: cosa si intende per "ORA"
        # ora è 19-19
        pioggia = [self.__dati[rec]['mm']
                   for rec in self.__dati
                   if dt19gp < rec <= dt19]
        pioggia_max = [sum(pioggia[i:i + 6])
                       for i in range(len(pioggia) - 6)
                       if sum(pioggia[i:i + 6])]

        mm_pioggia_max = max(pioggia_max) if pioggia_max else 0

        return mm8, mm14, mm19, mm, durata_ore, durata_minuti, mm_pioggia_max

    def __bollettino_decadale(self):
        with open(FOUT_DECADALE, 'w') as fout:

            for dal, al in ((0, 10), (10, 20), (20, None)):
                tabella1 = []
                tabella2 = []

                for giorno, rec1, rec2 in self.__dati_bollettino_decadale[dal:al]:
                    rigo1 = '%2s\t%s' % (giorno, '\t'.join(rec1))
                    tabella1.append(rigo1)

                    rigo2 = '%2s\t%s' % (giorno, '\t'.join(rec2))
                    tabella2.append(rigo2)

                tabella1 = '\n'.join(tabella1)
                tabella2 = '\n'.join(tabella2)

                scheda = '%s%s%s%s' % (tabella1, '\n' * 12, tabella2, '\n' * 3)
                scheda = scheda.replace('.', ',')
                scheda = scheda.replace(':', '.')

                fout.write(scheda)

    def __analizza_per_bollettino_mensile(self):
        anno = self.anno
        mese = self.mese
        # todo: ngiorni da calcolare
        ngiorni = 31

        bollettino = []
        lpress = []
        lt = []
        ltmin = []
        ltmax = []
        lur = []
        lvel = []
        lmm = []
        ldurata = []
        for giorno in range(1, ngiorni + 1):
            dal = datetime.datetime(anno, mese, giorno, 0)
            al = dal + datetime.timedelta(days=1)
            # pressione
            press = statistics.mean([float(self.__dati[dt]['pres'])
                                     for dt in self.__dati
                                     if dal < dt <= al and self.__dati[dt]['pres']])
            lpress.append(press)

            # temperatura
            t = statistics.mean([float(self.__dati[dt]['t'])
                                 for dt in self.__dati
                                 if dal < dt <= al and self.__dati[dt]['t']])
            tmin = min([float(self.__dati[dt]['tmin'])
                        for dt in self.__dati
                        if dal < dt <= al and self.__dati[dt]['tmin']])
            tmax = max([float(self.__dati[dt]['tmax'])
                        for dt in self.__dati
                        if dal < dt <= al and self.__dati[dt]['tmax']])
            lt.append(t)
            ltmin.append(tmin)
            ltmax.append(tmax)

            # umidita
            ur = statistics.mean([float(self.__dati[dt]['ur'])
                                  for dt in self.__dati
                                  if dal < dt <= al and self.__dati[dt]['ur']])
            lur.append(ur)

            # vento
            vdir, vvel = self.__calcola_vento_bollettino_mensile(dal, al)
            lvel.append(vvel)

            # eliofania & cielo
            eliof_assoluta = sum([float(self.__dati[dt]['eliof'])
                                  for dt in self.__dati
                                  if dal < dt <= al and self.__dati[dt]['eliof']]) / 60
            eliof_max = eliofania.eliofania_da_sun_ephemeris(anno)['%4i/%02i/%02i' % (anno, mese, giorno)]
            eliof_relativa = eliof_assoluta / eliof_max * 100

            if eliof_relativa > 80:
                cielo = 'Sereno'
            elif eliof_relativa > 60:
                cielo = 'Poco Nuvoloso'
            elif eliof_relativa > 40:
                cielo = 'Nuvoloso'
            elif eliof_relativa > 20:
                cielo = 'Molto Nuvoloso'
            else:
                cielo = 'Coperto'

            # mare
            if vvel <= 5:
                mare = 'Calmo'
            elif vvel <= 10:
                mare = 'Poco Mosso'
            elif vvel <= 15:
                mare = 'Mosso'
            else:
                mare = 'Molto Mosso'

            # pioggia
            mm, durata, durata_secondi = self.__calcola_pioggia_bollettino_mensile(dal, al)
            lmm.append(mm)
            ldurata.append(durata_secondi)

            # formattazione
            giorno = '%2i' % giorno
            press = '%.0f' % press
            t = '%.1f' % t
            tmin = '%.1f' % tmin
            tmax = '%.1f' % tmax
            ur = '%.0f' % ur
            vvel = '%.0f' % vvel
            mm = '%.1f' % mm if mm else ''

            rigo = (giorno, press, t, tmin, tmax, ur, vdir, vvel, cielo, mare, mm, durata)
            bollettino.append(rigo)

        # formattazione
        press = '%.0f' % statistics.mean(lpress)
        t = '%.1f' % statistics.mean(lt)
        tmin = '%.1f' % statistics.mean(ltmin)
        tmax = '%.1f' % statistics.mean(ltmax)
        ur = '%.0f' % statistics.mean(lur)
        vvel = '%.0f' % statistics.mean(lvel)
        mm = '%.1f' % sum(lmm)
        durata = sum(ldurata) / 60
        durata_hh = int(durata / 60)
        durata_mm = durata - durata_hh * 60
        durata = '%02i:%02i' % (durata_hh, durata_mm)

        rigo_medie = ('Medie', press, t, tmin, tmax, ur, '', vvel, '', 'Totale', mm, durata)
        bollettino.append(rigo_medie)
        self.__dati_bollettino_mensile = bollettino

    def __calcola_pioggia_bollettino_mensile(self, dal, al):
        mm = sum([float(self.__dati[dt]['mm'])
                  for dt in self.__dati
                  if dal < dt <= al])

        # todo: correggere durata per piogge che iniziano e finiscono nei giorni contigui
        durata = [rec
                  for rec in self.__dati
                  if dal < rec <= al and self.__dati[rec]['mm']]
        durata.sort()

        dt = datetime.timedelta(minutes=10)
        if durata:
            # orari_piogge = [[dalle_1, alle_1], [dalle_2, alle_2], ...]
            orari_piogge = [[durata[0] - dt, durata[0]]]

            for rec in durata[1:]:
                if rec - DT_PIOGGIA > orari_piogge[-1][1]:
                    orari_piogge.append([rec - dt, rec])
                else:
                    orari_piogge[-1][1] = rec

            durata_totale = sum([(al - dal).seconds for dal, al in orari_piogge])
            durata_totale_secondi = durata_totale
            durata_ore = durata_totale // (60 * 60)
            durata_minuti = (durata_totale % (60 * 60)) // 60
            durata_totale = '%s:%s' % (durata_ore, durata_minuti)

        else:
            durata_totale = ''
            durata_totale_secondi = 0

        return mm, durata_totale, durata_totale_secondi

    def __calcola_vento_bollettino_mensile(self, dal, al):
        velocita = statistics.mean([float(self.__dati[dt]['vvel'])
                                    for dt in self.__dati
                                    if dal < dt <= al]) * 3.6
        if velocita < 5.0:
            return ('-', velocita)
        else:
            vento = [(int(self.__dati[dt]['vdir']), float(self.__dati[dt]['vvel']))
                     for dt in self.__dati
                     if dal < dt <= al]

            ldirezioni = []
            for vd, vv in vento:
                d, v = self.__direzione_vento(vd, vv)
                ldirezioni.append(d)

            direzione_dominate = self.__vento_direzione_dominante(ldirezioni)

        return direzione_dominate, velocita

    def __vento_direzione_dominante(self, ldirezioni):
        direzioni = [(ldirezioni.count('N'), 'N'),
                     (ldirezioni.count('NO'), 'NO'),
                     (ldirezioni.count('O'), 'O'),
                     (ldirezioni.count('SO'), 'SO'),
                     (ldirezioni.count('S'), 'S'),
                     (ldirezioni.count('SE'), 'SE'),
                     (ldirezioni.count('E'), 'E'),
                     (ldirezioni.count('NE'), 'NE')
                     ]
        direzioni.sort(reverse=True)

        return direzioni[0][1]

    def __bollettino_mensile_csv(self):
        with open(FOUT_MENSILE_CSV, 'w') as fout:
            for rigo in self.__dati_bollettino_mensile:
                rigo = '%s\n' % ('\t'.join(rigo),)

                fout.write(rigo)

    def __bollettino_mensile_pdf(self):
        pdf.bollettino_mensile(anno=self.anno, mese=self.mese, dati=self.__dati_bollettino_mensile)

    def __analizza_per_bollettino_pioggia(self):
        anno = self.anno
        mese = self.mese
        dumb, ngiorni = calendar.monthrange(anno, mese)

        dal = datetime.datetime(anno, mese, 1, 0)
        al = dal + datetime.timedelta(days=ngiorni)

        durate = [x
                  for x in self.__dati
                  if dal <= x < al if float(self.__dati[x]['mm'])]
        durate.sort()

        dt = datetime.timedelta(minutes=10)

        # orari_piogge = [[dalle_1, alle_1], [dalle_2, alle_2], ...]
        orari_piogge = [[durate[0] - dt, durate[0]]]

        for rec in durate[1:]:

            if rec - DT_PIOGGIA > orari_piogge[-1][1]:
                orari_piogge.append([rec - dt, rec])
            else:
                orari_piogge[-1][1] = rec

        lpioggia = []
        for pioggia in orari_piogge:
            dalle, alle = pioggia

            if dalle.day == alle.day:
                ppioggia = self.__calcola_pioggia_bollettino_pioggia(pioggia)
                lpioggia.append(ppioggia)
            else:
                dalle2 = alle1 = datetime.datetime(alle.year, alle.month, alle.day, 0)
                ppioggia1 = self.__calcola_pioggia_bollettino_pioggia((dalle, alle1))
                ppioggia2 = self.__calcola_pioggia_bollettino_pioggia((dalle2, alle))
                lpioggia.append(ppioggia1)
                lpioggia.append(ppioggia2)

        dati = []
        mm_totali = durata_totale = 0
        mm_gionalieri = durata_giornaliera = 0
        mm_gionalieri_p = durata_giornaliera_p = 0
        for i, p in enumerate(lpioggia):
            giorno, dalle, alle, mm, durata, carattere = p
            mm_totali += mm
            durata_totale += durata

            if lpioggia[i - 1][0] == giorno:
                giorno_diverso = False
                giorno = '  '
                mm_gionalieri += mm
                durata_giornaliera += durata
            else:
                giorno_diverso = True
                giorno = '%i' % giorno
                mm_gionalieri_p = mm_gionalieri
                durata_giornaliera_p = durata_giornaliera
                mm_gionalieri = mm
                durata_giornaliera = durata

            dalle = dalle.strftime('%H:%M')
            alle = alle.strftime('%H:%M')

            mm = '%.1f' % mm

            ore = int(durata)
            minuti = (durata - ore) * 60
            durata = '%02i:%02.0f' % (ore, minuti)

            rigo = [giorno, dalle, alle, mm, durata, carattere]

            if giorno_diverso and mm_gionalieri_p:
                mm_gionalieri_p = '%.1f' % mm_gionalieri_p

                ore_giornaliere = int(durata_giornaliera_p)
                minuti_giornalieri = (durata_giornaliera_p - ore_giornaliere) * 60
                durata_giornaliera_p = '%02i:%02.0f' % (ore_giornaliere, minuti_giornalieri)

                dati[i - 1].extend([mm_gionalieri_p, durata_giornaliera_p])

            dati.append(rigo)

        mm_gionalieri = '%.1f' % mm_gionalieri

        ore_giornaliere = int(durata_giornaliera)
        minuti_giornalieri = (durata_giornaliera - ore_giornaliere) * 60
        durata_giornaliera = '%02i:%02.0f' % (ore_giornaliere, minuti_giornalieri)

        dati[i].extend([mm_gionalieri, durata_giornaliera])

        mm_totali = '%.1f' % mm_totali
        ore_totali = int(durata_totale)
        minuti_totali = (durata_totale - ore_totali) * 60
        durata_totale = '%02i:%02.0f' % (ore_totali, minuti_totali)

        dati.append(['', '', '', '', '', 'Totale', mm_totali, durata_totale])

        self.__dati_bollettino_pioggia = dati

    def __calcola_pioggia_bollettino_pioggia(self, pioggia):
        dalle, alle = pioggia

        giorno = dalle.day

        mm = sum([self.__dati[x]['mm']
                  for x in self.__dati
                  if dalle < x <= alle])

        durata = (alle - dalle).seconds / 60 / 60  # in ore

        # classificazione presa da https://it.wikipedia.org/wiki/Pioggia
        intensita = mm / durata
        if intensita <= 1:
            carattere = 'Pioviggine'
        elif intensita <= 2:
            carattere = 'Debole'
        elif intensita <= 4:
            carattere = 'Leggera'
        elif intensita <= 6:
            carattere = 'Moderata'
        elif intensita <= 10:
            carattere = 'Forte'
        elif intensita <= 30:
            carattere = 'Rovescio'
        else:
            carattere = 'Nubifragio'

        return giorno, dalle, alle, mm, durata, carattere

    def __bollettino_pioggia(self):
        with open(FOUT_PIOGGIA_CSV, 'w') as fout:
            for rigo in self.__dati_bollettino_pioggia:
                rigo = '%s\n' % ('\t'.join(rigo),)

                fout.write(rigo)

    def __bollettino_pioggia_pdf(self):
        pdf.bollettino_pioggia(anno=self.anno, mese=self.mese, dati=self.__dati_bollettino_pioggia)
