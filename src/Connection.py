import mysql.connector
from src import nacteni_konfigurace as conf

class Connection:
    def __init__(self):
        self.mycursor = None

        try:
            self.mydb = mysql.connector.connect(
                host=conf.nacti_host(),
                user=conf.nacti_user(),
                password=conf.nacti_password(),
                database=conf.nacti_databaze()
            )
        except:
            raise Exception("Spatna konfigurace nebo chyba v databazi")

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def get_connection(self):
        """
        pokud neni vytvoren kurzor, tak ho vytvori
        :return: kurzor
        """
        if self.mycursor == None:
            self.mycursor = self.mydb.cursor()
            self.mydb.autocommit = False
            return self
        else:
            return self

    def commit(self):
        """
        Metoda pro commit vsech zmen
        :return: pokud se vse provede, tak True
        """
        if self.mycursor == None:
            raise Exception("Spojeni s databazi nen vytvoreno")
        else:
            self.mydb.commit()
            return True

    def rollback(self):
        """
        Metoda pro rollback vsech zmen
        :return: pokud se vse provede, tak True
        """
        if self.mycursor == None:
            raise Exception("Spojeni s databazi nen vytvoreno")
        else:
            self.mydb.rollback()
            return True