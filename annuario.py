# 27.07.18
import calendar
import sqlite3 as lite
from pprint import pprint as pp

from costanti import *

TABELLA_MESE = r"""
\subsection{%(mese)s %(anno)i}

\begin{tabular}{c....ab}
\toprule
\multirow{2}{*}{\parbox{20mm}{\centering Giorno\\ del mese}}  &
\multicolumn{4}{c}{Temperatura}   &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{21mm}{\centering Pressione\\ Barometrica\\ ~[hPa]~}}}  &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{20mm}{\centering Tensione\\ di vapore\\ ~[mm]~}}}  \\

&
\multicolumn{4}{c}{[°C]}&

\\

\cmidrule{2-5}
& 
\multicolumn{1}{c}{minima} &
\multicolumn{1}{c}{massima} &
\multicolumn{1}{c}{media} & 
\multicolumn{1}{c}{escursione} & 
\\

\midrule

%(decade1)s

\midrule
\rowcolor{gray!15}
1\textsuperscript{a} decade & %(med_decade1)s\\
\midrule

%(decade2)s

\midrule
\rowcolor{gray!15}
2\textsuperscript{a} decade & %(med_decade2)s\\
\midrule

%(decade3)s

\midrule
\rowcolor{gray!15}
3\textsuperscript{a} decade & %(med_decade3)s\\
\midrule
\toprule \rowcolor{gray!30}
        
Mese & %(mensile)s\\
        
\bottomrule
\end{tabular}
\vfill
"""


class annuario_talsano(object):
    """
    annuario dal 1975 al 2006
    :return:
    """

    def __init__(self):
        pass

    def mese(self, mese, anno):
        dal = datetime.date(anno, mese, 1)
        al = datetime.date(anno, mese, calendar.monthrange(anno, mese)[1])

        cmd = '''SELECT data, t, tmin, tmax, pres, mm, durata, ur
                 FROM Giornaliero
                 WHERE data
                 BETWEEN '{dal}' AND '{al}'
                 '''.format(dal=dal,
                            al=al)
        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            dati = cur.execute(cmd).fetchall()

            return (dati)

    def latex_mese(self, mese, anno):
        dati = self.mese(mese, anno)

        d1 = self._decade(dati, 1)
        d2 = self._decade(dati, 2)
        d3 = self._decade(dati, 3)

        data = datetime.date(anno, mese, 1)
        cmd = '''SELECT t, tmin, tmax, pres, mm, durata
                 FROM Mensile
                 WHERE data = '{data}'
              '''.format(data=data)

        with lite.connect(NOME_DB) as con:
            cur = con.cursor()
            tmed, tmin, tmax, press, mm, durata = cur.execute(cmd).fetchall()[0]

            # todo correggere assenzza valori
            press = 0

        mensile = ' & '.join(('%.1f' % tmin, '%.1f' % tmax, '%.1f' % tmed, '%.1f' % (tmax - tmin),
                              '%.1f' % press))

        # ltx = TABELLA_MESE % (MESE[mese], anno, d1)
        ltx = TABELLA_MESE % ({'mese': MESE[mese],
                               'anno': anno,
                               'decade1': d1[0],
                               'decade2': d2[0],
                               'decade3': d3[0],
                               'med_decade1': d1[1],
                               'med_decade2': d2[1],
                               'med_decade3': d3[1],
                               'mensile': mensile
                               })

        return ltx

    def _decade(self, dati, decade):
        da = 10 * (decade - 1)
        a = da + 10

        if decade == 3:
            a = None

        righe = []
        dtmed = 0
        dtmin = 100
        dtmax = -100
        dtesc = 0
        dpress = 0
        dmm = 0
        ddurata = 0
        dur = 0
        for d in dati[da:a]:
            data, tmed, tmin, tmax, press, mm, durata, ur = d

            data = str(int(data[-2:]))
            tesc = tmax - tmin

            dtmed += tmed
            dtmin = tmin if tmin < dtmin else dtmin
            dtmax = tmax if tmax > dtmax else dtmax
            dtesc += tmax-tmin
            dpress += 0  # todo correggere assenza valori
            dmm += mm
            ddurata += durata
            dur += ur

            if press:
                press = str(press)
            else:
                press = ''

            rec = ' & '.join((data, str(tmin), str(tmax), str(tmed), '%.1f' % tesc, press, '\\\\\n'))
            righe.append(rec)

        righe = ''.join(righe)

        n = len(dati[da:a])
        dtmed /= n
        dtesc /= n
        dpress /= n
        dur /= n

        decadale = ' & '.join(
            ('%.1f' % dtmin, '%.1f' % dtmax, '%.1f' % dtmed, '%.1f' % dtesc, '%.1f' % dpress))

        return righe, decadale
