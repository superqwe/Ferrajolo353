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


def annuario_anno_t(dati):
    x = range(1975, 2006 + 1)

    fig, ax = plt.subplots()
    ax.plot(x, dati['tmax'], label='Massimo Assoluto', color=(1, 0, 0))
    ax.plot(x, dati['tq3'], label='3° Quartile', color=(1, .65, 0))
    ax.plot(x, dati['tmean'], label='Media', color=(1, 0, 1))
    ax.plot(x, dati['tmed'], label='Mediana', color=(0, .5, 0))
    ax.plot(x, dati['tq1'], label='1° Quartile', color=(0, 1, 1))
    ax.plot(x, dati['tmin'], label='Minimo Assoluto', color=(0, 0, 1))

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, )
    ax.grid(True)
    plt.show()
