from src import Connection
from src import Pozemek
Pozemek = Pozemek.Pozemek
from src import Misto_prace
Misto_prace = Misto_prace.Misto_prace
conn = Connection.Connection()
from src import Sousedstvi
Sousedstvi = Sousedstvi.Sousedstvi

def start():
    entity = ["Sousedstvi","Pozemek","Misto_prace"]
    c = conn.get_connection()
    c.mydb.start_transaction()
    while True:
        print("---------------------------------")
        print("Menu")
        i = 1
        for e in entity:
            print(str(i) + " - Pracovat se zaznamy " + e)
            i += 1
        print(str(i) + " - Ulozit zmeny")
        print(str(i + 1) + " - Zrusit zmeny")
        print(str(i+2) + " - Ukoncit")
        start_input: int = int(input())
        if type(start_input) != int or start_input <= 0 or start_input > i+2:
            print("Musite zadat cislo v rozmezi")
        if start_input == 1:
            s = Sousedstvi()
            entity_actions = ["Vypsat vsechno", "Vypsat podle mista","Zmenit souseda mistu prace","Smazat sousedstvi","Vlozit sousedstvi"]
            print("Co chcete se zaznamy v teto entite delat?")
            entita_input:int == int(input())
            i = 1
            for e in entity_actions:
                print(str(i) + " - " + e)
                i += 1

            print(str(i) + " - Zpet")
            entita_input: int = int(input())
            if type(entita_input) != int or entita_input <= 0 or entita_input > i:
                print("Musite zadat cislo v rozmezi")
            if entita_input == 1:
                print("---------------------------")
                s.printAll()
                print("---------------------------")

            if entita_input == 2:
                print("Napiste obec, cislo popisne")
                soused_obec:str = input("Obec:")
                soused_cislo_popisne:int = int(input("Cislo popisne:"))
                print("---------------------------")
                s.printByMisto(soused_obec,soused_cislo_popisne)
                print("---------------------------")
                if s.printByMisto(soused_obec,soused_cislo_popisne) == None:
                    print("Tato obec nema zaznamenane sousedstvi")

            elif entita_input == 3:
                print("Napiste obec, cislo popisne, cislo popisne stareho souseda a pak cislo popisne noveho souseda")
                soused_obec:str = input("Obec:")
                soused_cislo_popisne:int = input("Cislo popisne:")
                soused_stary: str = input("Cislo popisne stareho souseda:")
                soused_novy: str = input("Cislo popisne noveho souseda:")
                if s.update_Soused(soused_obec,soused_cislo_popisne,soused_stary,soused_novy) == True:
                    print("Zmeneno")
                else:
                    raise Exception("Nelze zmenit")

            elif entita_input == 4:
                print("Napiste obec, cislo popisne, cislo popisne souseda")
                delete_obec: str = input("Obec:")
                try:
                    delete_cislo_popisne: int = int(input("Cislo popisne:"))
                    delete_soused: str = int(input("Cislo popisne souseda:"))
                except:
                    raise TypeError("Cislo popisne musi byt int!")
                if s.delete(delete_obec,delete_cislo_popisne,delete_soused) == True:
                    print("Smazano")
                else:
                    raise Exception("Nelze smazat")

            elif entita_input == 5:
                print("Napiste obec, cislo popisne mista a cislo popisne souseda")
                insert_obec:str = input("Obec:")
                try:
                    insert_cislo_popisne: int = int(input("Cislo popisne:"))
                    insert_soused: str = int(input("Cislo popisne souseda:"))
                except:
                    print("Cislo popisne musi byt int!")
                if s.insert(insert_obec,insert_cislo_popisne,insert_soused) == True:
                    print("Pridano")
                else:
                    raise Exception("Nelze pridat")

        if start_input == 2:
            p = Pozemek()
            entity_actions = ["Vypsat vsechno", "Smazat", "Vlozit zaznam", "Importovat z csv souboru"]
            print("Co chcete se zaznamy v teto entite delat?")
            entita_input: int == int(input())
            i = 1
            for e in entity_actions:
                print(str(i) + " - " + e)
                i += 1
            print(str(i) + " - Zpet.")
            entita_input: int = int(input())
            if type(entita_input) != int or entita_input <= 0 or entita_input > i + 1:
                raise TypeError("Musite zadat cislo v rozmezi")
            if entita_input == 1:
                print("---------------------------")
                p.printAll()
                print("---------------------------")

            if entita_input == 2:
                try:
                    cislo: int = int(input("Cislo popisne pozemku:"))

                except:
                    print("Toto neni cislo")
                if p.delete(cislo) == True:
                    print("Uspesne smazano")
                else:
                    print("Chyba pri mazani")


            elif entita_input == 3:
                try:
                    cislo: int = int(input("Cislo popisne:"))
                    if p.insert(cislo) == True:
                        print("Uspesne vlozeno")
                except:
                    print("Toto neni cislo")

            elif entita_input == 4:
                path: str = input("Cesta k souboru:")
                if p.import_csv(path) == True:
                    print("Uspesne importovano")


        if start_input == 3:
            m = Misto_prace()
            entity_actions = ["Vypsat vsechno", "Smazat", "Vlozit zaznam", "Importovat z csv souboru","Vypsat pocet"]
            print("Co chcete se zaznamy v teto entite delat?")
            entita_input: int == int(input())
            i = 1
            for e in entity_actions:
                print(str(i) + " - " + e)
                i += 1
            print(str(i) + " - Zpet.")
            entita_input: int = int(input())
            if type(entita_input) != int or entita_input <= 0 or entita_input > i + 1:
                raise TypeError("Musite zadat cislo v rozmezi")
            if entita_input == 1:
                print("---------------------------")
                m.printAll()
                print("---------------------------")

            if entita_input == 2:
                obec: str = str(input("Obec:"))
                try:
                    cislo: int = int(input("Cislo popisne pozemku:"))
                    if m.delete(obec,cislo) == True:
                        print("Uspesne smazano")
                except:
                    print("Toto neni cislo")


            elif entita_input == 3:
                obec: str = str(input("Obec:"))
                ulice:str = str(input("Ulice:"))
                try:
                    cislo: int = int(input("Cislo popisne:"))
                    katastralni_uzemi = str(input("Katastralni uzemi:"))
                    cast_mesta:str = str(input("Cast mesta:"))
                    if m.insert(obec,ulice,cislo,katastralni_uzemi,cast_mesta) == True:
                        print("Uspesne vlozeno")
                except:
                    print("Toto neni cislo")

            elif entita_input == 4:
                path: str = input("Cesta k souboru:")
                try:
                    if p.import_csv(path) == True:
                        print("Uspesne importovano")
                except:
                    raise TypeError("Cislo popisne musi byt int!")

        elif start_input == 4:

            try:
                c.commit()
                print("Ulozeno")
            except:
                print("Nelze ulozit")

        elif start_input == 5:
            try:
                c.rollback()
                print("Zmeny zruseny")
            except:
                print("Nemate nic k zruseni")

        elif start_input == 6:
            print("Nashledanou")
            break

