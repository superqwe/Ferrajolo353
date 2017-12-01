# 14.11.17: rev0
import csv
import os
import time
from pprint import pprint as pp


def eliofania_da_sun_ephemeris(anno):
    fin = '%i.csv' % anno
    path = os.path.join('dati', fin)

    eliofania = {}
    with open(path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')

        for row in reader:
            data = time.strptime(row['data'], '%d/%m/%Y')
            data = time.strftime('%Y/%m/%d', data)
            ore_di_luce = float(row['ore_di_luce'].replace(',', '.'))
            eliofania[data] = ore_di_luce

    return eliofania


def __test():
    anno = 2016

    eliofania = eliofania_da_sun_ephemeris(anno)

    pp(eliofania)


if __name__ == '__main__':
    __test()
