from src import Connection
import csv
import re

conn = Connection.Connection()

class Misto_prace:
    def __init__(self):
        self.id: int = None
        self.obec: str = None
        self.ulice: str = None
        self.cislo_popisne:int = None
        self.katastralni_uzemi:str = None
        self.cast_mesta:str = None

    def insert(self, obec:str, ulice:str, cislo_popisne:int,katastralni_uzemi:str,cast_mesta:str):
        """
        metoda pro pridani zanzamu do tabulky misto_prace
        :param obec: nazev obce
        :param ulice: nazev ulice
        :param cislo_popisne: cislo popisne
        :param katastralni_uzemi: kod katastralniho uzemi
        :param cast_mesta: cast mesta("Sever","Vychod","Jih","Zapad")
        :return: pokud se vse provede, tak True
        """
        connection = conn.get_connection()
        sql = "insert into misto_prace(obec,ulice,cislo_popisne,katastralni_uzemi,cast_mesta)values(%s,%s,%s,%s,%s)"
        vals = (obec,ulice,cislo_popisne,katastralni_uzemi,cast_mesta)
        try:
            connection.mycursor.execute(sql, vals)
        except:
            raise ("Nelze vlozit misto prace")
        return True

    def printAll(self):
        """
        Vypsani vsech prvku z metody findAll
        :return:
        """
        for x in self.findAll():
            print("Obec: " + x.obec + ", Ulice: "+ x.ulice + ", Cislo popisne: " + str(x.cislo_popisne) + ", Katastralni uzemi: " + str(x.katastralni_uzemi) + ", Cast mesta: " + str(x.cast_mesta))

    def findAll(self):
        """
        metoda pro nalezeni vsech zaznamu z tabulky misto_prace a vlozeni do listu
        :return: list zaznamu
        """
        connection = conn.get_connection()
        sql = "SELECT * FROM misto_prace "
        connection.mycursor.execute(sql)
        myresult = connection.mycursor.fetchall()
        mista = []
        for x in myresult:
            m = Misto_prace()
            m.id = x[0]
            m.obec = x[1]
            m.ulice = x[2]
            m.cislo_popisne = x[3]
            m.katastralni_uzemi = x[4]
            m.cast_mesta = x[5]
            mista.append(m)


        return mista


    def update_obec(self, old_obec:str, cislo_popisne :int, new_obec:str):
        """
        Uprava obce u zanzamu tabulky misto_prace
        :param old_obec: stara obec
        :param cislo_popisne: cislo popisne
        :param new_obec: nova obec
        :return: pokud se vse provede, tak True
        """
        connection = conn.get_connection()
        sql = "update misto_prace set obec = %s where obec = %s and cislo_popisne = %s"
        vals = (new_obec,old_obec,cislo_popisne)
        try:
            connection.mycursor.execute(sql, vals)
        except:
            raise Exception("Nelze zmenit obec u tohoto mista")
        return True

    def delete(self, obec:str,cislo_popisne:int):
        """
        Smazani zaznamu z tabulky misto_prace
        :param obec: nazev obce
        :param cislo_popisne: cislo popisne obce
        :return: pokud se vse provede, tak True
        """
        connection = conn.get_connection()
        sql = "delete from misto_prace where obec = %s and cislo_popisne = %s"
        vals = (obec,cislo_popisne,)
        try:
            connection.mycursor.execute(sql, vals)
        except:
            raise Exception("Tento zaznam nelze smazat nebo zaznam s temito daty neexistuje")
        return True

    def import_csv(self,path:str):
        """
                Metoda pro importu vsech zaznamu z csv souboru do tabulky misto_prace
                :param path: cesta k souboru
                :return: pokud se vse provede, tak True
            """
        try:
            f = open(path, "r")
            reader = csv.DictReader(f)
        except:
            raise Exception("Nelze otevrit soubor")
        connection = conn.get_connection()

        if path.endswith(".csv") == False:
            raise Exception("Soubor musi byt csv!")

        for misto in reader:
            try:
                sql = "insert into misto_prace(obec,ulice,cislo_popisne,katastralni_uzemi,cast_mesta)values(%s,%s,%s,%s,%s);"
                vals = (misto["obec"], misto["ulice"], misto["cislo_popisne"], misto["katastralni_uzemi"],misto["cast_mesta"])
                connection.mycursor.execute(sql, vals)
            except:
                raise ("Nelze vlozit mista prace")
        f.close()
        return True