# 16.11.17: rev 0

import os
import sqlite3 as lite

from costanti import NOME_DB


class DB(object):
    def __init__(self):
        self.db = lite.connect(NOME_DB)
        self.cur = self.db.cursor()

    def crea_db(self):
        # todo: aggiungere vento filato ed eliofania teorica e relativa nelle tabelle da orario in su
        # todo: sostituire TIMESTAMP con DATETIME
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
                                         durata INT,
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
                                         durata INT,
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
                                          durata INT,
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
        except lite.OperationalError:
            print('tabella esistente: Eliofania')

        try:
            cmd = """CREATE  TABLE Pioggia(dalle TIMESTAMP NOT NULL,
                                           alle TIMESTAMP,
                                           mm FLOAT,
                                           durata INT)"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Pioggia')

        # tabelle Annuario Talsano
        try:
            cmd = """CREATE TABLE Annuario_Talsano_G(
                        data DATE NOT NULL,
                        tmed   FLOAT,
                        tmin   FLOAT,
                        tmax   FLOAT,
                        pres   FLOAT,
                        ur     FLOAT,
                        tens   FLOAT,
                        mm     FLOAT,
                        durata INT,
                        nuvol  FLOAT,
                        vvel   FLOAT,
                        vdir   TEXT,
                        vfil   INT
                    )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Annuario_G')

        try:
            cmd = """CREATE TABLE Annuario_Talsano_M(
                        data DATE NOT NULL,
                        tmed   FLOAT,
                        tmin   FLOAT,
                        tmax   FLOAT,
                        pres   FLOAT,
                        ur     FLOAT,
                        tens   FLOAT,
                        mm     FLOAT,
                        durata INT,
                        nuvol  FLOAT,
                        vvel   FLOAT,
                        vdir   TEXT,
                        vfil   INT
                    )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Annuario_M')

        try:
            cmd = """CREATE TABLE Annuario_Talsano_A(
                        data   INT,
                        tmed   FLOAT,
                        tmin   FLOAT,
                        tmax   FLOAT,
                        pres   FLOAT,
                        ur     FLOAT,
                        tens   FLOAT,
                        mm     FLOAT,
                        durata INT,
                        nuvol  FLOAT,
                        vvel   FLOAT,
                        vdir   TEXT,
                        vfil   INT
                    )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Annuario_A')

    def crea_tabelle_bollettino_crea(self):
        self.cur.execute('DROP TABLE IF EXISTS Bollettino1')
        self.cur.execute('DROP TABLE IF EXISTS Bollettino2')

        try:
            cmd = """CREATE  TABLE Bollettino1(data DATE NOT NULL,
                                               p8 FLOAT,
                                               p14 FLOAT,
                                               p19 FLOAT,
                                               ta8 FLOAT,
                                               tb8 FLOAT,
                                               tv8 FLOAT,
                                               ta14 FLOAT,
                                               tb14 FLOAT,
                                               tv14 FLOAT,
                                               ta19 FLOAT,
                                               tb19 FLOAT,
                                               tv19 FLOAT,
                                               u8 FLOAT,
                                               u14 FLOAT,
                                               u19 FLOAT,
                                               u_med FLOAT,
                                               tv_med FLOAT,
                                               t_min FLOAT,
                                               t_max FLOAT,
                                               t_med FLOAT,
                                               mm8 FLOAT,
                                               mm14 FLOAT,
                                               mm19 FLOAT,
                                               mm_tot FLOAT,
                                               durata TEXT,
                                               mm_max FLOAT,
                                               h_max INT,
                                               n1  FLOAT,
                                               n2 FLOAT
                                               )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Bollettino1')

        try:
            cmd = """CREATE  TABLE Bollettino2(data DATE NOT NULL,
                                               vd8 TEXT,
                                               vv8 FLOAT,
                                               vd14 TEXT,
                                               vv14 FLOAT,
                                               vd19 TEXT,
                                               vv19 FLOAT,
                                               km_tot FLOAT,
                                               km_med FLOAT,
                                               v_max FLOAT,
                                               h_v_max INT,
                                               n8 INT,
                                               n_tipo8 TEXT,
                                               n14 INT,
                                               n_tipo14 TEXT,
                                               n19 INT,
                                               n_tipo19 TEXT,
                                               n_tot FLOAT,
                                               smc FLOAT,
                                               e FLOAT,
                                               r  FLOAT,
                                               s TEXT,
                                               s_t  FLOAT
                                               )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Bollettino2')

    def crea_tabella_bollettino_mensile(self):
        self.cur.execute('DROP TABLE IF EXISTS Bollettino_Mensile')

        cmd = """
        CREATE TABLE Bollettino_Mensile(
        data INT,
        pres INT,
        t FLOAT,
        tmin FLOAT,
        tmax FLOAT,
        ur INT,
        vd TEXT,
        vv INT,
        cielo TEXT,
        mare TEXT,
        mm FLOAT,
        h TIME,        
        )
        """
        self.cur.execute(cmd)
        self.db.commit()

    def resetta(self):
        self.db.close()
        os.remove(NOME_DB)
        print('DB resettato')
        self.__init__()
        self.crea_db()

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
