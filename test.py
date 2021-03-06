# 23.11.17: rev0
import datetime
import unittest
from pprint import pprint as pp

import bollettino
import pioggia_util
import util
import vento_util
import pandas as pd


class test_pioggia_util(unittest.TestCase):
    def test_pioggia_per_tabella_oraria(self):
        # todo: da completare
        dal = datetime.datetime(2012, 4, 16)
        al = datetime.datetime(2012, 4, 17)

        risultato = pioggia_util.pioggia_per_tabella_oraria(dal, al)
        # self.assertEqual(True, True)


class test_util(unittest.TestCase):
    def test_timestamp2date(self):
        atteso = datetime.date(2012, 4, 16)
        risultato = util.timestamp2date('2012-04-16 08:10:00')
        self.assertEqual(risultato, atteso)

    def test_timestamp2datetime(self):
        atteso = datetime.datetime(2012, 4, 16, 8, 10)
        risultato = util.timestamp2datetime('2012-04-16 08:10:00')
        self.assertEqual(risultato, atteso)

    def test_minuti2ore_minuti(self):
        atteso = (5, 10)
        risultato = util.minuti2ore_minuti(60 * 5 + 10)
        self.assertEqual(risultato, atteso)


class test_vento_util(unittest.TestCase):
    def test_direzione_dominante(self):
        dati_vento = [
            ('2016-01-01', 1.811, 162),
            ('2016-01-01', 2.608, 326),
            ('2016-01-01', 0.414, 267),
            ('2016-01-01', 0.331, 102),
            ('2016-01-01', 1.982, 2),
            ('2016-01-01', 1.381, 104),
            ('2016-01-01', 0.227, 54),
            ('2016-01-01', 1.562, 6),
            ('2016-01-01', 1.086, 289),
            ('2016-01-01', 0.687, 129),
            ('2016-01-01', 0.986, 238),
            ('2016-01-01', 0.018, 109),
            ('2016-01-01', 1.684, 137),
            ('2016-01-01', 0.895, 329),
            ('2016-01-01', 2.838, 333),
            ('2016-01-01', 2.616, 197),
            ('2016-01-01', 1.277, 161),
            ('2016-01-01', 1.565, 2),
            ('2016-01-01', 1.066, 195),
            ('2016-01-01', 0.123, 126),
            ('2016-01-02', 1.188, 175),
            ('2016-01-02', 2.722, 207),
            ('2016-01-02', 1.266, 119),
            ('2016-01-02', 2.100, 360),
            ('2016-01-02', 2.743, 204),
            ('2016-01-02', 2.018, 33),
            ('2016-01-02', 0.977, 230),
            ('2016-01-02', 2.444, 102),
            ('2016-01-02', 2.604, 139),
            ('2016-01-02', 1.841, 330),
            ('2016-01-02', 0.931, 141),
            ('2016-01-02', 1.813, 347),
            ('2016-01-02', 1.418, 61),
            ('2016-01-02', 2.306, 174),
            ('2016-01-02', 1.824, 10),
            ('2016-01-02', 0.033, 152),
            ('2016-01-02', 2.556, 186),
            ('2016-01-02', 1.288, 15),
            ('2016-01-02', 0.929, 309),
            ('2016-01-02', 0.300, 364),
            ('2016-01-03', 0.946, 270),
            ('2016-01-03', 2.661, 315),
            ('2016-01-03', 0.296, 99),
            ('2016-01-03', 2.865, 94),
            ('2016-01-03', 0.590, 279),
            ('2016-01-03', 0.579, 114),
            ('2016-01-03', 0.456, 176),
            ('2016-01-03', 2.886, 27),
            ('2016-01-03', 0.763, 362),
            ('2016-01-03', 2.692, 65),
            ('2016-01-03', 0.302, 150),
            ('2016-01-03', 1.353, 212),
            ('2016-01-03', 1.536, 152),
            ('2016-01-03', 2.473, 131),
            ('2016-01-03', 2.536, 235),
            ('2016-01-03', 1.748, 290),
            ('2016-01-03', 2.352, 261),
            ('2016-01-03', 1.623, 281),
            ('2016-01-03', 2.708, 93),
            ('2016-01-03', 0.652, 202),
        ]

        discretizzazione = 'giornaliero'
        risultato_atteso = [('N', '2016-01-01'), ('N', '2016-01-02'), ('O', '2016-01-03')]

        result = vento_util.direzione_dominante(dati_vento, discretizzazione)
        self.assertEqual(risultato_atteso, result, 'test direzione dominante ok')

    def test_direzione_vento(self):
        # tipico
        atteso = 'NE', 5.0
        risultato = vento_util.direzione_vento(50, 5.0)
        self.assertEqual(risultato, atteso)

        # tipico senza correzione velocita per CALMA
        atteso = 'NE', 5.0
        risultato = vento_util.direzione_vento(50, 5.0, False)
        self.assertEqual(risultato, atteso)

        # caso vento CALMO con correzione velocita per CALMA
        atteso = '-', 0.0
        risultato = vento_util.direzione_vento(50, 1.0)
        self.assertEqual(risultato, atteso)

        # caso vento CALMO senza  correzione velocita per CALMA
        atteso = '-', 1.0
        risultato = vento_util.direzione_vento(50, 1.0, False)
        self.assertEqual(risultato, atteso)

    def test_vento_con_settori(self):
        # tipico
        dati = pd.DataFrame({'vdir': ['SE', 'SE', 'N', 'O', 'O', 'SE', 'SE', 'SE', 'N', 'N', 'C', 'C', 'C',
                                      'C', 'C', 'C', 'C', 'C']})
        atteso = 'SE'
        vento = vento_util.vento_con_settori(dati)
        risultato = vento.dominante
        self.assertEqual(risultato, atteso)


if __name__ == '__main__':
    unittest.main()
