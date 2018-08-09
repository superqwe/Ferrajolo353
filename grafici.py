# 01.08.18

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook
from pprint import pprint as pp


def annuario_mese_tmin(dati):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    mysym = dict( markersize=2)
    # mysym = dict(marker='+', color='red', markersize=5,
    #              linestyle='-')
    plt.boxplot(dati,
                patch_artist=True,  # fill with color
                labels=labels,
                notch=False,
                flierprops=mysym,
                )

    plt.grid(True)
    # plt.show()
    plt.savefig('annuario/tmin_mese.svg', format='svg')


def annuario_mese_tmax(dati):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    fig, ax = plt.subplots()
    ax.boxplot(dati,
                vert=True,  # vertical box alignment
                patch_artist=True,  # fill with color
                labels=labels)  # will be used to label x-ticks

    ax.grid(True)
    # plt.show()
    plt.savefig('annuario/tmax_mese.pdf', format='pdf')


def annuario_mese_tmed(dati):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    fig, ax = plt.subplots()
    ax.boxplot(dati,
                vert=True,  # vertical box alignment
                patch_artist=True,  # fill with color
                labels=labels)  # will be used to label x-ticks

    ax.grid(True)

    # plt.show()
    plt.savefig('annuario/tmed_mese.pdf', format='pdf')


def annuario_anno_tmed(dati):
    x = range(1975, 2006 + 1)

    fig, ax = plt.subplots()
    ax.plot(x, dati['tmax'], label='Massimo', color=(1, 0, 0))
    ax.plot(x, dati['tq3'], label='3° Quartile', color=(1, .65, 0))
    ax.plot(x, dati['tmean'], label='Media', color=(1, 0, 1))
    ax.plot(x, dati['tmed'], label='Mediana', color=(0, .5, 0))
    ax.plot(x, dati['tq1'], label='1° Quartile', color=(0, 1, 1))
    ax.plot(x, dati['tmin'], label='Minino', color=(0, 0, 1))

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, )
    ax.grid(True)

    # plt.show()
    plt.savefig('annuario/tmed_anno.pdf', format='pdf')
