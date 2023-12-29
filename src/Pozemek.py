from src import Connection
conn = Connection.Connection()
import csv

class Pozemek:
    def __init__(self):
        self.cislo:int = None

    def insert(self, cislo):
        """
        Vlozeni noveho pozemku
        :param cislo: cislo popisne pozemku
        :return: pokud se vse provede, tak True
        """
        connection = conn.get_connection()
        sql = "insert into pozemek values(%s)"
        vals = (cislo,)
        try:
            connection.mycursor.execute(sql, vals)
        except:
            raise Exception("Tento pozemek jiz existuje nebo byla zadana spatna hodnota")
        return True

    def printAll(self):
        """
        Vypsani vsech prvky z metody findAll
        :return:
        """
        for x in self.findAll():
            print(x.cislo)

    def findAll(self):
        """
        Nalezeni vsech zaznamu metody pozemek a nasledne predano do listu
        :return: list zaznamu
        """
        connection = conn.get_connection()
        sql = "SELECT * FROM pozemek"
        connection.mycursor.execute(sql)
        myresult = connection.mycursor.fetchall()
        pozemky = []
        for x in myresult:
            p = Pozemek()
            p.cislo = x[0]
            pozemky.append(p)
        return pozemky



    def delete(self, cislo):
        """
        metoda pro smazani daneho zaznamu z tabulky pozemek
        :param cislo: cislo pozemku
        :return: pokud se vse provede, tak True
        """
        connection = conn.get_connection()
        sql = "delete from pozemek where cislo = %s;"
        vals = (cislo,)
        try:
            connection.mycursor.execute(sql, vals)
        except:
            raise Exception("Nelze smazat pozemek")
        return True



    def import_csv(self,path:str):
        """
        Metoda pro importu vsech zaznamu z csv souboru do tabulky pozemek
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


        for pozemek in reader:
            try:
                sql = "insert into pozemek values(%s)"
                vals = (pozemek["cislo"],)
                try:
                    connection.mycursor.execute(sql, vals)
                except:
                    connection.mydb.rollback()
                    raise ("Nelze vlozit mista prace")
            except:
                raise Exception("Chyba v souboru nebo jeden z pozemku jiz existuje")
        f.close()
        return True
