# 16.11.17: rev 0

import datetime
import os
import sqlite3 as lite

from pprint import pprint as pp

from costanti import NOME_DB


class DB(object):
    def __init__(self):
        self.db = lite.connect(NOME_DB)
        self.cur = self.db.cursor()

    def crea_db(self):
        try:
            cmd = """CREATE TABLE Raw(data TIMESTAMP NOT NULL,
                                      t FLOAT,
                                      tmin FLOAT,
                                      tmax FLOAT,
                                      pres FLOAT,
                                      mm FLOAT,
                                      ur FLOAT,
                                      eliof FLOAT,
                                      pir FLOAT,
                                      vvel FLOAT,
                                      vdir INT
                                      )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Raw')

        try:
            cmd = """CREATE TABLE Orario(data TIMESTAMP NOT NULL,
                                         t FLOAT,
                                         tmin FLOAT,
                                         tmax FLOAT,
                                         pres FLOAT,
                                         mm FLOAT,
                                         ur FLOAT,
                                         eliof FLOAT,
                                         pir FLOAT,
                                         vvel FLOAT,
                                         vdir TEXT
                                         )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Orario', )

        tabelle = ('Giornaliero', 'Mensile')

        for tabella in tabelle:
            try:
                cmd = """CREATE TABLE %s(data DATE NOT NULL,
                                         t FLOAT,
                                         tmin FLOAT,
                                         tmax FLOAT,
                                         pres FLOAT,
                                         mm FLOAT,
                                         ur FLOAT,
                                         eliof FLOAT,
                                         pir FLOAT,
                                         vvel FLOAT,
                                         vdir TEXT
                                         )""" % tabella
                self.cur.execute(cmd)
                self.db.commit()
            except lite.OperationalError:
                print('tabella esistente:', tabella)

        try:
            cmd = """CREATE TABLE Annuale(data INT NOT NULL,
                                          t FLOAT,
                                          tmin FLOAT,
                                          tmax FLOAT,
                                          pres FLOAT,
                                          mm FLOAT,
                                          ur FLOAT,
                                          eliof FLOAT,
                                          pir FLOAT,
                                          vvel FLOAT,
                                          vdir TEXT
                                          )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Annuale')

        try:
            cmd = """CREATE TABLE Eliofania(data DATE NOT NULL,
                                            elio INT
                                            )"""
            self.cur.execute(cmd)
            self.db.commit()
            # print('tabella creata: Eliofania')
        except lite.OperationalError:
            print('tabella esistente: Eliofania')

        try:
            cmd = """CREATE  TABLE Pioggia(dalle TIMESTAMP NOT NULL,
                                           alle TIMESTAMP,
                                           mm FLOAT,
                                           durata TIME)"""
            self.cur.execute(cmd)
            self.db.commit()
            # print('tabella creata: Pioggia')
        except lite.OperationalError:
            print('tabella esistente: Pioggia')

    # def interroga(self, tabella, dal, al=None, campi=[], solo_orari=True):
    #     if campi:
    #         campi = list(campi)
    #         campi.insert(0, 'data')
    #         campi = ', '.join(campi)
    #     else:
    #         campi = '*'
    #
    #     if al:
    #         al = datetime.datetime(al.year, al.month, al.day, 23, 59, 59)
    #     else:
    #         al = datetime.datetime(dal.year, dal.month, dal.day, 23, 59, 59)
    #
    #     if solo_orari:
    #         solo_orari = """AND ( strftime('%M', data) = '00' OR
    #                               strftime('%M', data) = '59')"""
    #     else:
    #         solo_orari = ''
    #
    #     cmd = """
    #              SELECT {campi}
    #              FROM {tabella}
    #              WHERE data
    #              BETWEEN '{dal}' AND '{al}'
    #              {solo_orari}
    #           """.format(campi=campi,
    #                      tabella=tabella,
    #                      dal=dal,
    #                      al=al,
    #                      solo_orari=solo_orari)
    #
    #     return self.cur.execute(cmd)

    def resetta(self):
        self.db.close()
        os.remove(NOME_DB)
        print('DB resettato')
        self.__init__()
        self.crea_db()


if __name__ == '__main__':
    db = DB()
    db.crea_db()
    # db.ricrea_db()
