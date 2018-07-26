# 27.07.18
import calendar
import sqlite3 as lite
from pprint import pprint as pp

from costanti import *

TABELLA_MESE = r"""
\subsection{%s %i}

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

%s

\midrule
                \rowcolor{gray!15}
                1\textsuperscript{a} decade & 8.2 & 15.3 & 11.5 & 7.1 & 1011.9 & 8.7\\
                \midrule

11 & 4.7 & 15.2 & 9.5 & 10.5 & 1018.4 &8.6 \\
\midrule
                \rowcolor{gray!15}
                2\textsuperscript{a} decade & 6.6 & 12.6 & 9.5 & 6.0 & 1014.4 & 8.0\\
                \midrule

21 & 10.0 & 14.0 & 11.4 & 4.0 & 1013.9 &8.7 \\
\midrule
        \rowcolor{gray!15}
        3\textsuperscript{a} decade & 9.2 & 15.1 & 12.1 & 5.9 & 1008.1 & 9.7\\
        \midrule
\toprule \rowcolor{gray!30}
        Mese & 8.0 & 14.4 & 11.1 & 6.4 & 1011.3 & 8.8\\
        
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

        d1 =self._decade(dati, 1)
        d2 =self._decade(dati, 2)
        d3 =self._decade(dati, 3)

        ltx = TABELLA_MESE % (MESE[mese], anno, d1)
        print(ltx)

    def _decade(self, dati, decade):
        da = 10 * (decade-1)
        a = da+10

        if decade==3:
            a=None


        righe = []
        for d in dati[da:a]:
            data, tmed, tmin, tmax, press, mm, durata, ur = d

            data = str(int(data[-2:]))

            if press:
                press = str(press)
            else:
                press = ''

            rec = ' & '.join((data, str(tmin), str(tmax), str(tmed), '%.1f' % (tmax - tmin), press, '\\\\\n'))
            righe.append(rec)

        righe = ''.join(righe)

        return righe
