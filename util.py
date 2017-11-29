# 28.11.17: rev0
import datetime

from costanti import *


def timestamp2datetime(timestamp):
    return datetime.datetime.strptime(timestamp, DATETIME_PF)


def minuti2ore_minuti(minuti):
    ore = minuti // 60
    minuti = minuti % 60

    return (ore , minuti)
