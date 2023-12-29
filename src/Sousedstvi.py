from src import Connection
from src import Pozemek
Pozemek = Pozemek.Pozemek
from src import Misto_prace
Misto_prace = Misto_prace.Misto_prace
conn = Connection.Connection()

class Sousedstvi:
    def __init__(self):
        self.id:int = None
        self.pozemek:Pozemek = None
        self.misto_prace:Misto_prace = None


    def insert(self,obec:str, cislo_popisne :int, pozemek_cislo:int):
        """
        Metoda pro vlozeni zaznamu do tabulky obec
        :param obec: nazev obce mista
        :param cislo_popisne: cislo popisne mista
        :param pozemek_cislo: cislo popisne pozemku, ktery je sousedem daneho mista
        :return: pokud se vse provede, tak True
        """
        connection = conn.get_connection()
        sql = "SELECT misto_prace.id FROM misto_prace where misto_prace.obec = %s and misto_prace.cislo_popisne = %s"
        vals = (obec, cislo_popisne)
        try:
            connection.mycursor.execute(sql, vals)
            misto_id = connection.mycursor.fetchall()[0][0]
        except:
            raise Exception("Nelze nalezt misto s temito udaji")

        connection = conn.get_connection()
        sql = "insert into sousedstvi(id_misto_prace,id_pozemek) values (%s,%s)"
        vals = (misto_id,pozemek_cislo)
        try:
            connection.mycursor.execute(sql, vals)
        except:
            raise Exception("Nelze pridat sousedstvi")
        return True

    def printAll(self):
        """
        Metoda pro vypsani vsech zaznamu z metody findAll
        :return: None
        """
        for x in self.findAll():
            print("Obec pozemku: " + x.misto_prace.obec + "\nKatastralni uzemi: " + str(x.misto_prace.katastralni_uzemi) +
                  "\nPozemek, na kterem se bude provadet prace: Ulice: " + x.misto_prace.ulice + ", Cislo popisne: " + str(x.misto_prace.cislo_popisne) +
                  "\nCislo popisne dotceneho pozemku: " + str(x.pozemek.cislo) + "\nCast mesta: " + str(x.misto_prace.cast_mesta))

            print()


    def findAll(self):
        """
        Metoda pro vyhledani vsech zaznamu z tabulky sousedstvi
        :return: list vsech zaznamu
        """
        connection = conn.get_connection()
        sql = "SELECT sousedstvi.id,misto_prace.id,misto_prace.obec,misto_prace.ulice,misto_prace.cislo_popisne,misto_prace.katastralni_uzemi,misto_prace.cast_mesta,pozemek.cislo FROM sousedstvi " \
              "inner join misto_prace on misto_prace.id = sousedstvi.id_misto_prace " \
              "inner join pozemek on pozemek.cislo = sousedstvi.id_pozemek"
        try:
            connection.mycursor.execute(sql)
            myresult = connection.mycursor.fetchall()

        except:
            raise Exception("Nelze ziskat vsechny zaznamy z tabulky sousedstvi")
        sousedstvi = []
        for x in myresult:
            s = Sousedstvi()
            m = Misto_prace()
            s.id = x[0]
            m.id = x[1]
            m.obec = x[2]
            m.ulice = x[3]
            m.cislo_popisne = x[4]
            m.katastralni_uzemi = x[5]
            m.cast_mesta = x[6]
            p = Pozemek()
            p.cislo = x[7]
            s.pozemek = p
            s.misto_prace = m
            sousedstvi.append(s)

        return sousedstvi

    def findByMisto(self,obec:str,cislo_popisne:int):
        """
        Vyhledani zaznamu na zaklade dvou atributu z mista
        :param obec: nazev obce mista
        :param cislo_popisne: cislo popisne mista
        :return: list vsech odpovidajicich zaznamu
        """
        connection = conn.get_connection()
        sql = "SELECT sousedstvi.id,misto_prace.id,misto_prace.obec,misto_prace.ulice,misto_prace.cislo_popisne,misto_prace.katastralni_uzemi,misto_prace.cast_mesta,pozemek.cislo FROM sousedstvi inner join misto_prace on misto_prace.id = sousedstvi.id_misto_prace inner join pozemek on pozemek.cislo = sousedstvi.id_pozemek where misto_prace.obec = %s and misto_prace.cislo_popisne = %s"
        vals = (obec,cislo_popisne)
        try:
            connection.mycursor.execute(sql, vals)
            myresult = connection.mycursor.fetchall()
        except:
            raise Exception("Nelze najit sousedy tohoto mista")
        sousedstvi = []
        for x in myresult:
            s = Sousedstvi()
            m = Misto_prace()
            s.id = x[0]
            m.id = x[1]
            m.obec = x[2]
            m.ulice = x[3]
            m.cislo_popisne = x[4]
            m.katastralni_uzemi = x[5]
            m.cast_mesta = x[6]
            p = Pozemek()
            p.cislo = x[7]
            s.pozemek = p
            s.misto_prace = m
            sousedstvi.append(s)

        return sousedstvi

    def printByMisto(self, obec:str,cislo_popisne:int):
        """
        vypsani vsech zaznamu z metody findByMisto
        :param obec: nazev obce
        :param cislo_popisne: cislo popisne obce
        :return:
        """
        if self.findByMisto(obec,cislo_popisne) == []:
            return None
        for x in self.findByMisto(obec,cislo_popisne):
            print(
                "Obec pozemku: " + x.misto_prace.obec + "\nKatastralni uzemi: " + str(x.misto_prace.katastralni_uzemi) +
                "\nPozemek, na kterem se bude provadet prace: Ulice: " + x.misto_prace.ulice + ", Cislo popisne: " + str(
                    x.misto_prace.cislo_popisne) +
                "\nCislo popisne dotceneho pozemku: " + str(x.pozemek.cislo) + "\nCast mesta: " + str(
                    x.misto_prace.cast_mesta))

            print()
        return True



    def update_Soused(self, obec:str, cislo_popisne :int,stary_soused:int, novy_soused:int):
        """
        Uprava zanznamu v tabulce sousedstvi
        :param obec: nazev obce mista
        :param cislo_popisne: cislo popisne mista
        :param stary_soused: cislo souseda, ktere chceme zmenit
        :param novy_soused: cislo, na ktere chceme souseda zmenit
        :return: pokud se vse provede, tak True
        """
        connection = conn.get_connection()
        sql = "SELECT misto_prace.id FROM sousedstvi inner join misto_prace on misto_prace.id = sousedstvi.id_misto_prace where misto_prace.obec = %s and misto_prace.cislo_popisne = %s and sousedstvi.id_pozemek = %s"
        vals = (obec, cislo_popisne,stary_soused)
        try:
            connection.mycursor.execute(sql, vals)
            misto_id = connection.mycursor.fetchall()[0][0]
            if misto_id == 0:
                raise Exception("Toto misto nema souseda s timto cislem")
        except:
            raise Exception("Nelze nalezt misto s temito udaji nebo sousedem")


        connection = conn.get_connection()
        sql = "update sousedstvi set id_pozemek = %s where id_misto_prace = %s"
        vals = (novy_soused,misto_id)
        try:
            connection.mycursor.execute(sql, vals)
        except:
            raise Exception("Nelze zmenit souseda")
        return True

    def delete(self,obec:str, cislo_popisne:int, soused:int):
        """
        metoda pro smazani zaznamu z tabulky sousedstvi
        :param obec: nazev obce mista
        :param cislo_popisne: cislo popisne mista
        :param soused: cislo popisne souseda
        :return: pokud se vse provede, tak true
        """
        connection = conn.get_connection()
        sql = "SELECT misto_prace.id FROM misto_prace where misto_prace.obec = %s and misto_prace.cislo_popisne = %s"
        vals = (obec, cislo_popisne)
        try:
            connection.mycursor.execute(sql, vals)
            misto_id = connection.mycursor.fetchall()[0][0]
        except:
            raise Exception("Nelze nalezt misto s temito udaji")

        connection = conn.get_connection()
        sql = "delete from sousedstvi where id_misto_prace = %s and id_pozemek = %s"
        vals = (misto_id, soused)
        try:
            connection.mycursor.execute(sql, vals)
        except:
            raise Exception("Nelze smazat sousedstvi")
        return True


