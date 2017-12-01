# 01.12.17: rev0
import sqlite3 as lite
from pprint import pprint as pp
from costanti import *


def eliofania_assoluta_orario(dal, al):
    cmd = """
    SELECT giornaliero.eliof / eliofania.elio * 100, eliofania.data
    FROM eliofania
    LEFT OUTER JOIN giornaliero
    ON eliofania.data = giornaliero.data
    WHERE eliofania.data BETWEEN '{da}' AND '{a}' 
    """.format(da=dal, a=al)

    with lite.connect(NOME_DB) as con:
        cur = con.cursor()
        res = cur.execute(cmd).fetchall()

        return res
