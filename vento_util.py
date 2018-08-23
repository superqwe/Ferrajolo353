from pprint import pprint as pp
import pandas as pd

CALMA = 5 / 3.6


def direzione_dominante(dati_in, discretizzazione=True):
    """
    Calcola la direzione dominante per i giorni dati escludendo i record con velocità <= CALMA o None
    
    :param dati_in: [(data1, vel11, dir11), (data1, vel12, dir12), ..., (data2, vel21, dir22),...]
    :param discretizzazione: se True calcola la direzione dominate per data 
    :return: [(direzione_dominate1, data1), (direzione_dominate2, data2), ...]
    """

    def ordina_per_data(x):
        return x[1]

    dati = {}

    if discretizzazione:

        for data, vel, direzione in dati_in:

            vel = vel if vel else 0

            if vel > CALMA:

                if data in dati:
                    dati[data].append(direzione)
                else:
                    dati[data] = [direzione, ]

    # pp(dati)
    dir_dominate = []
    for data, direzioni in dati.items():

        ldirezioni = []
        for direzione in direzioni:
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

            ldirezioni.append(direzione)

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
        # pp(direzioni)

        dir_dominate.append((direzioni[0][1], data))

    dir_dominate.sort(key=ordina_per_data)
    return dir_dominate


def direzione_vento(direzione, velocita, velocita_0_calma=True):
    """

    :param direzione:
    :param velocita:
    :param velocita_0_calma: True --> velocita = 0 se velocita < CALMA
    :return:
    """
    if velocita > CALMA:
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

    else:
        if velocita_0_calma:
            velocita = 0.0
        return '-', velocita


class vento_con_settori(object):
    def __init__(self, dati):
        """
        calcola la direzione dominate
        :param dati: ['N', 'N', 'C', 'NO', ...]
        """
        self.dati = dati

        self._direzione_dominante()

    def _direzione_dominante(self):
        occorrenze = self.dati['vdir'].value_counts()
        occorrenze = zip(occorrenze.values, occorrenze.index)

        for c, d in occorrenze:
            dominante = d

            # scarta il valore C
            if d == 'C':
                continue

            break

        self.dominante = dominante
