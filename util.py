# 28.11.17: rev0
import datetime

from costanti import *


def timestamp2datetime(timestamp):
    """
    timestamp2datetime('2012-01-02 03:40:00') --> datetime.datetime(2012, 1, 2, 3 ,40, 0)
    :param timestamp:
    :return:
    """

    return datetime.datetime.strptime(timestamp, DATETIME_PF)


def timestamp2date(timestamp):
    """
    timestamp2datetime('2012-01-02 03:40:00') --> datetime.date(2012, 1, 2)
    :param timestamp:
    :return:
    """

    return datetime.datetime.strptime(timestamp, DATETIME_PF).date()


def timestamp2time(timestamp):
    """
    timestamp2datetime('2012-01-02 03:40:00') --> datetime.time(3,4,0)
    :param timestamp:
    :return:
    """

    return datetime.datetime.strptime(timestamp, DATETIME_PF).time()


def minuti2ore_minuti(minuti):
    ore = minuti // 60
    minuti = minuti % 60

    return (ore, minuti)
