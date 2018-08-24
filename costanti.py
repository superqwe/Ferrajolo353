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
FOUT_ANNUARIO_GIORNI = 'annuario/tabelle_dati_giornalieri.tex'
FOUT_ANNUARIO_MESI = 'annuario/tabelle_dati_mensili.tex'
FOUT_ANNUARIO_ANNI = 'annuario/tabelle_dati_annuali.tex'

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

# annuario
ANNO_INIZIO_ANNUARIO = 1975
ANNO_FINE_ANNUARIO = 2006

# tabelle annuario
TABELLA_DATI_GIORNALIERI = r"""
\subsection{%(mese)s %(anno)i}

\begin{sideways}
\begin{tabular}{c....a...e..c.}
\toprule
\multirow{2}{*}{\parbox{11mm}{\centering Giorno\\ del mese}}  &
\multicolumn{4}{c}{Temperatura}   &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{19mm}{\centering Pressione\\ Barometrica\\ ~[hPa]~}}}  &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{13mm}{\centering Umidità\\ relativa\\ ~[\%%]~}}} &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{14mm}{\centering Tensione\\ di vapore\\ ~[XXX]~}}} &
\multicolumn{2}{c}{Precipitazioni} &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{17mm}{\centering Nuvolosit\`a\\ ~[decimi]~}}}&
\multicolumn{3}{c}{Vento}
\\

\cmidrule{9-10}
\cmidrule{12-14}
&
\multicolumn{4}{c}{[°C]}&
&
&
&
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{9mm}{\centering totale\\ ~[mm]~}}} &
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{13mm}{\centering durata\\ ~[minuti]~}}}&
&
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{12mm}{\centering velocit\`a\\ ~[km/h]~}}} &
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{14mm}{\centering direzione\\ ~}}}&
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{9mm}{\centering filato\\ ~[km]~}}}
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

%(decade2)s

\midrule

%(decade3)s


\bottomrule
\end{tabular}
\end{sideways}
\vfill
"""

TABELLA_DATI_MENSILI = r"""
\subsection{%(anno)i}

\begin{sideways}
\begin{tabular}{c....a...e..c.}
\toprule
\multirow{2}{*}{\parbox{11mm}{\centering Mese}}  &
\multicolumn{4}{c}{Temperatura}   &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{19mm}{\centering Pressione\\ Barometrica\\ ~[hPa]~}}}  &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{13mm}{\centering Umidità\\ relativa\\ ~[\%%]~}}} &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{14mm}{\centering Tensione\\ di vapore\\ ~[XXX]~}}} &
\multicolumn{2}{c}{Precipitazioni} &
\multicolumn{1}{c}{\multirow{3}{*}{\parbox{17mm}{\centering Nuvolosit\`a\\ ~[decimi]~}}}&
\multicolumn{3}{c}{Vento}
\\

\cmidrule{9-10}
\cmidrule{12-14}
&
\multicolumn{4}{c}{[°C]}&
&
&
&
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{9mm}{\centering totale\\ ~[mm]~}}} &
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{13mm}{\centering durata\\ ~[minuti]~}}}&
&
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{12mm}{\centering velocit\`a\\ ~[km/h]~}}} &
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{14mm}{\centering direzione\\ ~}}}&
\multicolumn{1}{c}{\multirow{2}{*}{\parbox{9mm}{\centering filato\\ ~[km]~}}}
\\

\cmidrule{2-5}
&
\multicolumn{1}{c}{minima} &
\multicolumn{1}{c}{massima} &
\multicolumn{1}{c}{media} &
\multicolumn{1}{c}{escursione} &
\\


\midrule

%(mensile)s


\bottomrule
\end{tabular}
\end{sideways}
"""
