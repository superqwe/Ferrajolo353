# 01.08.18

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook
from pprint import pprint as pp


def annuario_t_mese(dati, parametro, formato='pdf'):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    mysym = dict(markersize=2)

    fig, ax = plt.subplots()
    bxplt = ax.boxplot(dati,
                       patch_artist=True,
                       labels=labels,
                       notch=False,
                       flierprops=mysym)

    colori_box = {'tmax': 'red',
                  'tmed': 'green',
                  'tmin': 'blue'}

    colori_medians = {'tmax': 'salmon',
                      'tmed': 'palegreen',
                      'tmin': 'skyblue'}
    # pp(bxplt)
    for box in bxplt['boxes']:
        box.set_facecolor(colori_box[parametro])

    for medians in bxplt['medians']:
        medians.set_color(colori_medians[parametro])

    ax.grid(True)
    plt.ylim(-8, 41)
    # plt.show()
    plt.savefig('annuario/%s_mese.%s' % (parametro, formato), format=formato)


def annuario_t_anno(dati, parametro):
    x = range(1975, 2006 + 1)
    ncol = 3
    fig, ax = plt.subplots()
    ax.plot(x, dati['tmax'], label='Massimo', color=(1, 0, 0))
    ax.plot(x, dati['tq3'], label='3° Quartile', color=(1, .65, 0))
    ax.plot(x, dati['tmean'], label='Media', color=(1, 0, 1))
    ax.plot(x, dati['tmed'], label='Mediana', color=(0, .5, 0))
    ax.plot(x, dati['tq1'], label='1° Quartile', color=(0, 1, 1))
    ax.plot(x, dati['tmin'], label='Minino', color=(0, 0, 1))

    for anno, fliers in enumerate(dati['fliers'], start=1975):
        if fliers:
            ax.scatter(anno, fliers, label='Anomalia')
            ncol += 1

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=ncol)
    ax.grid(True)
    plt.ylim(-8, 41)

    # plt.show()
    plt.savefig('annuario/%s_anno.pdf' % parametro, format='pdf')
