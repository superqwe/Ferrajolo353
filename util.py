# 28.11.17: rev0
import datetime

from costanti import *


def timestamp2datetime(timestamp):
    return datetime.datetime.strptime(timestamp, DATETIME_PF)
