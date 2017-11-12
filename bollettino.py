# 09.11.17: rev0
# 10.11.17
# 12.11.17

import csv

import datetime

from pprint import pprint as pp

# se tra un dato di pioggia rilevato ed un altro non supera questo tempo, allora la pioggia è continua
DT_PIOGGIA = datetime.timedelta(minutes=30)
FOUT = 'decadale.csv'


class Bollettino(object):
    def __init__(self, mese):
        self.mese = int(mese[2:])
        self.anno = 2000 + int(mese[:2])
        self.__fin = '%sm.txt' % mese
        self.__leggi_csv()
        self.__analizza_per_bollettino_decadale()
        self.__bollettino_decadale()

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
                vvel = float(row['TARANTO VEL V 10m (MED) m/s'] if row['TARANTO VEL V 10m (MED) m/s'] else
                             None)
                vdir = row['TARANTO DIR V 10m (MED) GN'] if row['TARANTO DIR V 10m (MED) GN'] else None
                ur = row['TARANTO UM 2m (MED) %'] if row['TARANTO UM 2m (MED) %'] else None
                eliof = float(row['TARANTO ELIOF (MED) min']) if row['TARANTO ELIOF (MED) min']  else None
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
            tmin = min([float(self.__dati[datetime.datetime(anno, mese, giorno, h)]['tmin'])
                        for h in range(24)
                        if datetime.datetime(anno, mese, giorno, h) in self.__dati])
            tmax = max([float(self.__dati[datetime.datetime(anno, mese, giorno, h)]['tmax'])
                        for h in range(24)
                        if datetime.datetime(anno, mese, giorno, h) in self.__dati])

            mm8, mm14, mm19, mm, durata_ore, durata_minuti, mm_pioggia_max = self.__calcola_pioggia(anno,
                                                                                                    mese,
                                                                                                    giorno)

            record1 = (
                self.__dati[datetime.datetime(anno, mese, giorno, 8)]['pres'],
                self.__dati[datetime.datetime(anno, mese, giorno, 14)]['pres'],
                self.__dati[datetime.datetime(anno, mese, giorno, 19)]['pres'],
                '',
                '',
                self.__dati[datetime.datetime(anno, mese, giorno, 14)]['t'],
                '',
                '',
                self.__dati[datetime.datetime(anno, mese, giorno, 19)]['t'],
                '',
                '',
                self.__dati[datetime.datetime(anno, mese, giorno, 8)]['ur'],
                self.__dati[datetime.datetime(anno, mese, giorno, 14)]['ur'],
                self.__dati[datetime.datetime(anno, mese, giorno, 19)]['ur'],
                '',
                '',
                '%.1f' % tmin,
                '%.1f' % tmax,
                '',
                '%.1f' % mm8,
                '%.1f' % mm14,
                '%.1f' % mm19,
                '%.1f' % mm,
                '%.0f' % durata_ore,
                '%.0f' % durata_minuti,
                '%.1f' % mm_pioggia_max,
                '',
            )

            km, velocita_media, velocita_max, orario = self.__calcola_vento(anno, mese, giorno)

            #  todo: da chiarire se l'eliofania è dalle 19-19 o dalle 0-24 --- ora è 19-19
            # todo: chidere unità di misura dell'eliofania MINUTI od ORE --- ora è ORE
            dt = datetime.datetime(anno, mese, giorno, 0)
            dt19gp = dt - datetime.timedelta(hours=5)
            dt19 = datetime.datetime(anno, mese, giorno, 19)

            eliofania = sum([self.__dati[dt]['eliof']
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
                self.__dati[datetime.datetime(anno, mese, giorno, 8)]['vdir'],
                '%.1f' % self.__dati[datetime.datetime(anno, mese, giorno, 8)]['vvel'],
                self.__dati[datetime.datetime(anno, mese, giorno, 14)]['vdir'],
                '%.1f' % self.__dati[datetime.datetime(anno, mese, giorno, 14)]['vvel'],
                self.__dati[datetime.datetime(anno, mese, giorno, 19)]['vdir'],
                '%.1f' % self.__dati[datetime.datetime(anno, mese, giorno, 19)]['vvel'],
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
                '%.3f' % eliofania,
                '%.3f' % radiazione
            )

            bollettino.append((giorno, record1, record2))

        self.__dati_bollettino_decadale = bollettino

    def __calcola_vento(self, anno, mese, giorno):
        #  todo: da chiarire se i km percorsi sono da dalle 19-19 o dalle 0-24 --- ora è 19-19
        dt = datetime.datetime(anno, mese, giorno, 0)
        dt19gp = dt - datetime.timedelta(hours=5)
        dt19 = datetime.datetime(anno, mese, giorno, 19)

        velocita = [self.__dati[dt]['vvel'] * 3.6
                    for dt in self.__dati
                    if dt19gp < dt <= dt19]
        km = sum(velocita) / 6
        tempo = len([self.__dati[dt]['vvel']
                     for dt in self.__dati
                     if dt19gp < dt <= dt19 if self.__dati[dt]['vvel']]) / 6
        velocita_media = 0 if not tempo else sum(velocita) / tempo

        # todo: verificare se esiste il dato di velocità max
        velocita_max, orario = max([(self.__dati[dt]['vvel'] * 3.6, dt.strftime('%H:%M'))
                                    for dt in self.__dati
                                    if dt19gp < dt <= dt19])

        return km, velocita_media, velocita_max, orario

    def __calcola_pioggia(self, anno, mese, giorno):
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
            print(tabella1)
            print(tabella2)
            print()
