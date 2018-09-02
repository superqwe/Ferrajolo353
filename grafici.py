from pprint import pprint as pp

import matplotlib.pyplot as plt


def annuario_t_mese(dati, parametro, formato='pdf'):
    # todo obsoleto
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    colori_box = {'tmax': 'red',
                  'tmed': 'green',
                  'tmin': 'blue'}

    colori_medians = {'tmax': 'salmon',
                      'tmed': 'palegreen',
                      'tmin': 'skyblue'}

    box_sym = dict(facecolor=colori_box[parametro])
    cap_sym = dict(color='black')
    flier_sym = dict(markersize=2, markeredgecolor=colori_box[parametro])
    median_sym = dict(color=colori_medians[parametro])
    whisker_sym = dict(color=colori_box[parametro])

    fig, ax = plt.subplots()
    ax.boxplot(dati,
               patch_artist=True,
               labels=labels,
               notch=False,
               boxprops=box_sym,
               capprops=cap_sym,
               flierprops=flier_sym,
               medianprops=median_sym,
               whiskerprops=whisker_sym)

    # todo tracciare solo asse x
    # ax.grid(True)
    plt.ylim(-11, 41)
    # plt.show()
    plt.savefig('annuario/grafici/%s_mese.%s' % (parametro, formato), format=formato)


def annuario_t_mese2(dati, formato='pdf'):
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    titolo = {0: 'Temperatura Massima',
              1: 'Temperatura Media',
              2: 'Temperatura Minima'}

    grandezza = {0: 'tmax',
                 1: 'tmed',
                 2: 'tmin'}

    colori_box = {'tmax': 'OrangeRed',
                  'tmed': 'green',
                  'tmin': 'RoyalBlue'}

    colori_medians = {'tmax': 'salmon',
                      'tmed': 'palegreen',
                      'tmin': 'skyblue'}

    plt.figure(figsize=(8.3, 11.7), dpi=600)
    # plt.figure()

    for x in range(3):
        plt.subplot(311 + x)

        #todo spostare i *_sym in constanti
        box_sym = dict(color=colori_box[grandezza[x]], facecolor=colori_box[grandezza[x]])
        cap_sym = dict(color='black')
        flier_sym = dict(markersize=2, markeredgecolor=colori_box[grandezza[x]])
        mean_sym = dict(marker='+', markeredgecolor='black')
        median_sym = dict(color=colori_medians[grandezza[x]])
        whisker_sym = dict(color=colori_box[grandezza[x]])

        plt.title(titolo[x])
        plt.ylim(-8, 41)
        plt.grid(axis='y')
        plt.ylabel('[°C]')

        plt.boxplot(dati[x],
                    patch_artist=True,
                    labels=labels,
                    notch=False,
                    boxprops=box_sym,
                    capprops=cap_sym,
                    flierprops=flier_sym,
                    medianprops=median_sym,
                    whiskerprops=whisker_sym,
                    showmeans=True,
                    meanprops=mean_sym,
                    meanline=False)

    plt.savefig('annuario/grafici/%s_mese.%s' % ('t', formato), format=formato, dpi=600)
    # plt.show()


def annuario_t_anno(dati, parametro):
    # todo obsoleto
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
    # ax.grid(True)
    plt.ylim(-8, 41)

    plt.show()
    # plt.savefig('annuario/grafici/%s_anno.pdf' % parametro, format='pdf')


def annuario_t_anno2(dati):
    # todo sistemare etichette asse x
    labels = range(1975, 2006 + 1)

    plt.figure(figsize=(8.3, 11.7), dpi=600)
    # plt.figure()

    titolo = {0: 'Temperatura Massima',
              1: 'Temperatura Media',
              2: 'Temperatura Minima'}

    grandezza = {0: 'tmax',
                 1: 'tmed',
                 2: 'tmin'}

    colori_box = {'tmax': 'OrangeRed',
                  'tmed': 'green',
                  'tmin': 'RoyalBlue'}

    colori_medians = {'tmax': 'salmon',
                      'tmed': 'palegreen',
                      'tmin': 'skyblue'}

    for x in range(3):
        plt.subplot(311 + x)

        # todo spostare i *_sym in constanti
        box_sym = dict(color=colori_box[grandezza[x]], facecolor=colori_box[grandezza[x]])
        cap_sym = dict(color='black')
        flier_sym = dict(markersize=2, markeredgecolor=colori_box[grandezza[x]])
        mean_sym = dict(marker='+', markeredgecolor='black')
        median_sym = dict(color=colori_medians[grandezza[x]])
        whisker_sym = dict(color=colori_box[grandezza[x]])

        plt.title(titolo[x])
        plt.ylim(-8, 41)
        plt.grid(axis='y')
        plt.ylabel('[°C]')

        plt.boxplot(dati[x],
                    patch_artist=True,
                    # labels=labels,
                    notch=False,
                    boxprops=box_sym,
                    capprops=cap_sym,
                    flierprops=flier_sym,
                    medianprops=median_sym,
                    whiskerprops=whisker_sym,
                    showmeans=True,
                    meanprops=mean_sym,
                    meanline=False)

    # plt.show()
    plt.savefig('annuario/grafici/t_anno.pdf', format='pdf')


def annuario_p_anno(dati):
    mean = dati[1][0]['mean']
    med = dati[1][0]['med']
    q3 = dati[1][0]['q3']
    q1 = dati[1][0]['q1']
    whishi = dati[1][0]['whishi']
    whislo = dati[1][0]['whislo']

    x = range(1975, 2006 + 1)
    xs = [1975 - .35, 2006 + .35]
    ncol = 4

    fig, ax = plt.subplots()

    ax.fill_between(xs, (whishi, whishi), (whislo, whislo), color=(.5, .85, .85))
    ax.fill_between(xs, (q3, q3), (q1, q1), color=(.75, 1, 1))

    ax.bar(x, dati[0], label='Annuale', color=(0, .5, 1))

    ax.plot(xs, (mean, mean), label='Media', color=(1, 0, 1))
    ax.plot(xs, (med, med), label='Mediana', color=(0, 1, 0))

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=ncol)
    # ax.grid(True)

    # plt.show()
    plt.savefig('annuario/grafici/%s_anno.pdf' % 'mm', format='pdf')


def annuario_p_mese(dati, formato='pdf'):
    parametro = 'mm'
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    mysym = dict(markersize=2)

    fig, ax = plt.subplots()
    bxplt = ax.boxplot(dati,
                       patch_artist=True,
                       labels=labels,
                       notch=False,
                       flierprops=mysym)

    colori_box = {'mm': (0, .5, 1)}

    colori_medians = {'mm': 'skyblue'}
    # pp(bxplt)
    for box in bxplt['boxes']:
        box.set_facecolor(colori_box[parametro])

    for medians in bxplt['medians']:
        medians.set_color(colori_medians[parametro])

    # ax.grid(True)
    # plt.ylim(-8, 41)

    # plt.show()
    plt.savefig('annuario/grafici/%s_mese.%s' % (parametro, formato), format=formato)


def annuario_pg_anno(dati):
    mean = dati[1][0]['mean']
    med = dati[1][0]['med']
    q3 = dati[1][0]['q3']
    q1 = dati[1][0]['q1']
    whishi = dati[1][0]['whishi']
    whislo = dati[1][0]['whislo']

    x = range(1975, 2006 + 1)
    xs = [1975 - .35, 2006 + .35]
    ncol = 4

    fig, ax = plt.subplots()

    ax.fill_between(xs, (whishi, whishi), (whislo, whislo), color=(.5, .85, .85))
    ax.fill_between(xs, (q3, q3), (q1, q1), color=(.75, 1, 1))

    ax.bar(x, dati[0], label='Annuale', color=(0, .5, 1))

    ax.plot(xs, (mean, mean), label='Media', color=(1, 0, 1))
    ax.plot(xs, (med, med), label='Mediana', color=(0, 1, 0))

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=ncol)
    # ax.grid(True)

    # plt.show()
    plt.savefig('annuario/grafici/%s_anno.pdf' % 'pg', format='pdf')


def annuario_pg_mese(dati, formato='pdf'):
    parametro = 'gp'
    labels = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']

    mysym = dict(markersize=2)

    fig, ax = plt.subplots()

    bxplt = ax.boxplot(dati,
                       patch_artist=True,
                       labels=labels,
                       notch=False,
                       flierprops=mysym)

    colori_box = {'gp': (0, .5, 1)}

    colori_medians = {'gp': 'skyblue'}

    for box in bxplt['boxes']:
        box.set_facecolor(colori_box[parametro])

    for medians in bxplt['medians']:
        medians.set_color(colori_medians[parametro])

    # ax.grid(True)

    # plt.show()
    plt.savefig('annuario/grafici/%s_mese.%s' % (parametro, formato), format=formato)


def annuario_pf_anno(dati, formato='pdf'):
    parametro = 'gf'
    fig, ax = plt.subplots()

    # bins = [0.2, 0.4, 0.6, 0.8, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22,
    #         24, 26, 28, 30, 40, 50]
    bins = [0.2, 0.4, 0.6, 0.8, 1, 5, 10, 20, 50]
    ax.hist(dati,
            bins,
            density=True,
            cumulative=True,
            )

    # plt.grid(True)
    # plt.show()
    plt.savefig('annuario/grafici/%s_anno.%s' % (parametro, formato), format=formato)
