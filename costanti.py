import datetime

# parse/format datetime.datetime
DATETIME_PF = '%Y-%m-%d %H:%M:%S'
DATE_PF = '%Y-%m-%d'
TIME_SHORT_PF = '%H:%M'

# intervalli di tempo
DT = datetime.timedelta(minutes=10)
DT_50MIN = datetime.timedelta(minutes=50)
DT_GIORNO = datetime.timedelta(days=1)
DT_ORA = datetime.timedelta(hours=1)

# se tra un dato di pioggia rilevato ed un altro non supera questo tempo, allora la pioggia è continua
DT_PIOGGIA = datetime.timedelta(minutes=30)

# file I/O
NOME_DB = 'Annuario.sqlite'
FOUT_CREA = '%i-%02i.csv'
FANNUARIO = 'annuario/anni.tex'

# mesi
MESE = {1: 'Gennaio',
        2: 'Febbraio',
        3: 'Marzo',
        4: 'Aprile',
        5: 'Maggio',
        6: 'Giugno',
        7: 'Luglio',
        8: 'Agosto',
        9: 'Settembre',
        10: 'Ottobre',
        11: 'Novembre',
        12: 'Dicembre'}

# tabelle annuario


TABELLA_MESE = r"""
\subsection{%(mese)s %(anno)i}

\begin{tabular}{c....a..e}
\toprule
\multirow{2}{*}{\parbox{20mm}{\centering Giorno\\ del mese}}  &
\multicolumn{4}{c}{Temperatura}   &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{21mm}{\centering Pressione\\ Barometrica\\ ~[hPa]~}}}  &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{20mm}{\centering Umidità\\ relativa\\ ~[\%%]~}}} &
\multicolumn{2}{c}{Precipitazioni}
\\

\cmidrule{8-9}
&
\multicolumn{4}{c}{[°C]}&
&
&
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{20mm}{\centering totale\\ ~[mm]~}}} &
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{20mm}{\centering durata\\ ~[minuti]~}}}\\

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

TABELLA_MESE2 = r"""
\subsection{%(mese)s %(anno)i}

\begin{sideways}
\begin{tabular}{c....a..e}
\toprule
\multirow{2}{*}{\parbox{20mm}{\centering Giorno\\ del mese}}  &
\multicolumn{4}{c}{Temperatura}   &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{21mm}{\centering Pressione\\ Barometrica\\ ~[hPa]~}}}  &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{20mm}{\centering Umidità\\ relativa\\ ~[\%%]~}}} &
\multicolumn{2}{c}{Precipitazioni}
\\

\cmidrule{8-9}
&
\multicolumn{4}{c}{[°C]}&
&
&
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{20mm}{\centering totale\\ ~[mm]~}}} &
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{20mm}{\centering durata\\ ~[minuti]~}}}\\

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

%(decade2)s

\midrule

%(decade3)s


\bottomrule
\end{tabular}
\end{sideways}
\vfill
"""
