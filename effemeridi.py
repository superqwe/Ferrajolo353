# 14.11.17: rev0
import csv
import os
import time
from pprint import pprint as pp


class Effemeridi(object):
    def __init__(self):
        pass

    def effemeridi_da_sun_ephemeris(self, anno):
        fin = '%i.csv' % anno
        path = os.path.join('dati', fin)

        effemeridi = {}
        with open(path, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter='\t')

            for row in reader:
                data = time.strptime(row['data'], '%d/%m/%Y')
                data = time.strftime('%Y/%m/%d', data)
                ore_di_luce = float(row['ore_di_luce'].replace(',', '.'))
                effemeridi[data] = ore_di_luce

        return effemeridi


def test():
    anno = 2017
    mese = 1

    effemeridi = Effemeridi()
    effe = effemeridi.effemeridi_da_sun_ephemeris(anno)
    pp(effe)


if __name__ == '__main__':
    test()
