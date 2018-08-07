# 01.08.18

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook
from pprint import pprint as pp


def annuario_mese_tmin(dati):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    mysym = dict(marker='+', color='red', markersize=5,
                 linestyle='-')
    plt.boxplot(dati,
                patch_artist=True,  # fill with color
                labels=labels,
                notch=True,
                flierprops=mysym)

    plt.show()

    stats = cbook.boxplot_stats(dati, labels=labels, )


def annuario_mese_tmax(dati):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    plt.boxplot(dati,
                vert=True,  # vertical box alignment
                patch_artist=True,  # fill with color
                labels=labels)  # will be used to label x-ticks

    plt.show()


def annuario_mese_med(dati):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    plt.boxplot(dati,
                vert=True,  # vertical box alignment
                patch_artist=True,  # fill with color
                labels=labels)  # will be used to label x-ticks

    plt.show()

def annuario_anno_tmin(dati):
    pass