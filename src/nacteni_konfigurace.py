import json


def nacti_soubor():
    """
    Funkce pro nacteni celeho konfiguracniho souboru
    """
    conf_text = ""
    try:
        conf = open("conf/config.conf", "r")
    except:
        raise Exception("Nelze nacist konfiguracni soubor")
    else:
        for line in conf:
            conf_text += line
        conf.close()
        return conf_text


def nacti_host():
    """
    Funkce pro nacteni from hosta ze souboru
    """
    try:
        data = json.loads(nacti_soubor())
        return data['host']
    except:
        raise Exception("Nelze nacist from host databaze z konfiguracniho souboru")



def nacti_user():
    """
    Funkce pro nacteni uzivatele ze souboru
    """
    try:
        data = json.loads(nacti_soubor())
        return data['user']
    except:
        raise Exception("Nelze nacist username k pripojeni k databazi z konfiguracniho souboru")


def nacti_password():
    """
    Funkce pro nacteni hesla ze souboru
    """
    try:
        data = json.loads(nacti_soubor())
        return data['password']
    except:
        raise Exception("Nelze nacist heslo k pripojeni k databazi z konfiguracniho souboru")


def nacti_databaze():
    """
    Funkce pro nacteni nazvu databaze ze souboru
    """
    try:
        data = json.loads(nacti_soubor())
        return data['database']
    except:
        raise Exception("Nelze nacist to nazev databaze z konfiguracniho souboru")



