import datetime
from pprint import pprint as pp

# from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def go(anno=None, mese=None, dati=None):
    # PAGE_HEIGHT = defaultPageSize[1]
    # PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    pageinfo = "platypus example"

    MESE = {1: 'Gennaio',
            2: 'Febbraio',
            3: 'Marzo',
            4: 'Aprile',
            5: 'Maggio',
            6: 'Giugno',
            7: 'Luglio',
            8: 'Agosto',
            9: 'Settembre',
            10: 'Ottobre',
            11: 'Novembre',
            12: 'Dicembre',
            None: ''}

    doc = SimpleDocTemplate("phello.pdf")
    style = styles["Normal"]
    pdfmetrics.registerFont(TTFont('Arial', 'ARIAL.TTF'))
    pdfmetrics.registerFont(TTFont('ArialNarrow', 'ARIALN.TTF'))
    pdfmetrics.registerFont(TTFont('ArialNarrowBold', 'ARIALNB.TTF'))
    pdfmetrics.registerFont(TTFont('BookmanOldStyle', 'BOOKOS.TTF'))
    pdfmetrics.registerFont(TTFont('BookmanOldStyleBold', 'BOOKOSB.TTF'))
    h1 = PS(name='Heading1', font='BookmanOldStyle', fontSize=16, leading=20, alignment=1)
    h2 = PS(name='Heading2', font='BookmanOldStyleBold', fontSize=18, leading=20, alignment=1, spaceAfter=10)
    h3 = PS(name='Heading3', font='BookmanOldStyle', fontSize=14, leading=20, alignment=1, spaceAfter=15)
    p_data = PS(name='Paragrafo', font='BookmanOldStyle')

    title1 = Paragraph('Osservatorio Meteorologico e Geofisico di Taranto', h1)
    title2 = Paragraph('<b>"Luigi Ferrajolo"</b>', h2)
    title3 = Paragraph('BOLLETTINO MENSILE - %s %s' % (MESE[mese], anno), h3)

    dati_tabella = [
        ['Data', 'Pressione', 'Temperatura', '', '', 'Umidità', 'Vento', '', 'Cielo', 'Mare',
         'Precipitazioni', ''],
        ['', 'a 0°', 'media', 'minima', 'massima', 'relativa', 'direzione', 'vel. media', '', '', 'pioggia',
         'durata', ],
        ['', '[hPA]', '[°C]', '[°C]', '[°C]', '[\%]', 'dominante', '[km/h]', '', '', '[mm]', '[hh:mm]', ]
    ]
    if dati:
        dati_tabella.extend(dati)

    stile_tabella = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'ArialNarrow'),
        ('FONT', (0, 0), (-1, 0), 'ArialNarrowBold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOX', (0, 0), (0, -1), 1, colors.black),
        ('BOX', (1, 0), (1, -1), 1, colors.black),
        ('BOX', (2, 0), (4, -1), 1, colors.black),
        ('BOX', (5, 0), (5, -1), 1, colors.black),
        ('BOX', (6, 0), (7, -1), 1, colors.black),
        ('BOX', (8, 0), (8, -1), 1, colors.black),
        ('BOX', (9, 0), (9, -1), 1, colors.black),
        ('BOX', (10, 0), (11, -1), 1, colors.black),

        # ('BOX', (0, 0), (-1, 2), 1, colors.black),
        ('BOX', (0, 3), (-1, 12), 1, colors.black),
        ('BOX', (0, 23), (-1, -1), 1, colors.black),
        # ('BOX', (0, 0), (-1, -1), 1, colors.black),

        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),

        ('SPAN', (2, 0), (4, 0)),
        ('SPAN', (6, 0), (7, 0)),
        ('SPAN', (10, 0), (11, 0)),
    ])

    tabella = Table(dati_tabella, style=stile_tabella)

    data = Paragraph('Taranto, lì %s' % (datetime.date.today().strftime('%d/%m/%Y'),), p_data)
    firma1 = Paragraph('IL DIRETTORE', style)
    firma2 = Paragraph('(Dott. Vittorio Semeraro)', style)
    pie = Paragraph('via Duomo, 181 - 74100 Taranto --- tel/fax: 099/4608278 --- '
                    'email: vittoriosemeraro@virgilio.it', style)
    Story = [title1, title2, title3, tabella, data, firma1, firma2, pie]

    doc.build(Story)

if __name__ == '__main__':
    go()
