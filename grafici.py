# 01.08.18

import matplotlib.pyplot as plt
import numpy as np


def annuario_mese_tmin(dati):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    mysym = dict(marker='+', markerfacecolor='red', markersize=3,linewidth=1,
                  linestyle='none')
    plt.boxplot(dati,
                patch_artist=True,  # fill with color
                labels=labels,
                notch=True,
                flierprops=mysym)
    # plt.violinplot(dati,
    #                vert=True,  # vertical box alignment
    #                # patch_artist=True,  # fill with color
    #                # labels=labels)  # will be used to label x-ticks
    #                showmeans=True,
    #                showmedians=True,
    #                bw_method='scott')
    plt.show()


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
