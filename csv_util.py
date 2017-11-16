# 14.11.17: rev0

import csv
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


def test():
    fin = 'eliofania.csv'

    eliofania = eliofania_da_sun_ephemeris(fin)

    # pp(eliofania)
    a = list(eliofania)
    pp(a)


if __name__ == '__main__':
    test()
