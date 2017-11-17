# 14.11.17: rev0

import csv
import datetime
import os
import time
from pprint import pprint as pp


def eliofania_da_sun_ephemeris(file_input, as_list=False):
    path = os.path.join('dati', file_input)

    eliofania = {}
    with open(path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')

        for row in reader:
            data = time.strptime(row['data'], '%d/%m/%Y')
            data = time.strftime('%Y/%m/%d', data)
            ore_di_luce = float(row['ore_di_luce'].replace(',', '.'))
            eliofania[data] = ore_di_luce

    if as_list:
        leliofania = []
        for k in eliofania.keys():
            leliofania.append((k, eliofania[k]))
        leliofania.sort()

        return leliofania

    return eliofania


def leggi_csv(file_in):
    path = os.path.join('dati', file_in)

    with open(path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')

        dati = []
        errori = []
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

                dati.append([data, t, tmin, tmax, pres, mm, ur, vvel, vdir, eliof, pir])

            except ValueError:
                print('dato mancante', row['GIORNO'], row['ORA'])
                errori.append(giorno)

    return dati, errori


def test():
    fin = 'eliofania.csv'

    eliofania = eliofania_da_sun_ephemeris(fin)

    # pp(eliofania)
    a = list(eliofania)
    pp(a)


if __name__ == '__main__':
    test()
