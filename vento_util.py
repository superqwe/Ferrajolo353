# 21.11.17: rev0

from pprint import pprint as pp

CALMA = 5 / 3.6


def direzione_dominante(dati_in, discretizzazione=''):
    def ordina_per_data(x):
        return x[1]

    dati = {}

    if discretizzazione == 'giornaliero':

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
