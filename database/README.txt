# Praktická maturitní zkouška

**Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30**
**Školní rok 2022/2023**
---
Jméno a příjmeni: Jakub Hrubý
Třída: C4c
Kontakt: jakub.hruby@centrum.cz
---

## Úvod
Databázi dokladu objednávky prací vodohospodářské společnosti Dobříš jsem se rozhodl vymodelovat v Oracle Datamodeler a návrh databáze v MySQL Workbench


## Analýza
Analýza se nachází v souboru analýza.txt


## E-R model
př:
konceptuální model databáze se nachází v /img/konceptualni.png
relační model databáze se nachází v /img/relacni.png

## Entitní integrita
Každá entita má svůj přidělený unikátní primární klíč, který se sám inkrementuje.


## Role a uživatelská oprávnění
SQL skript se nachází v sql/users.sql
- zadavac_objednavek - ma pristup do tabulek objednavka, misto_prace, objednavatel - select,update,delete,insert
- zadavac_sousedu - ma pristup pouze do tabulek sousedstvi, pozemek - select,update,delete,insert
- manazer - ma pristup k cele databazi


## Doménová integrita

** objednavatel
- jmeno_nazev_firmy - libovolné znaky, maximálně však 20 znaků, not null
- prijmeni - libovolné znaky, maximálně však 20 znaků
- ulice - libovolné znaky, maximálně však 40 znaků, not null
- cislo_popisne - datový typ int, minimálně 1 a maximálně 99999, not null
- mesto - libovolné znaky, maximálně však 40 znaků, not null
- psc - libovolné znaky, maximálně však 5 znaků, not null
- ico - libovolné znaky, maximálně však 8 znaků
- dic - libovolné znaky, maximálně však 10 znaků
- telefon - datový typ int, minimálně 100000000 a maximálně 999999999, not null
- fax - datový typ int, not null
- email - libovolné znaky, maximálně však 319 znaků
- platce_dph - datový typ boolean, not null

** misto_prace
- obec - libovolné znaky, maximálně však 40 znaků, not null
- ulice - libovolné znaky, maximálně však 40 znaků, not null
- cislo_popisne - datový typ int, minimálně 1 a maximálně 99999, not null
- katastralni_uzemi - libovolná čísla, maximálně však 6 znaků, not null
- psc - libovolné znaky, minimálně 10000 a maximálně 99999, not null

** dotceny_pozemek
- cislo - primary key, datový typ int, not null, unique

** objednavka
- souvisi_zakon - datový typ boolean, not null
- souvisi_ekonomicka_cinnost - datový typ boolean, not null
- zprac_osobni_udaje - datový typ boolean, not null
- datum_potvrzeni - datový typ date(YYYY-MM-DD), not null, musí být menší nebo roven aktualnímu datumu
- misto_potvrzeni - libovolné znaky, maximálně však 40 znaků, not null


## Referenční integrita
př:
** Návrh obsahuje několik cizích klíčů, které jsou uvedeny níže
- 'id_pozemek' - ON DELETE CASCADE
- 'id_misto_prace' - ON DELETE CASCADE
- 'id_druh_prace' - ON DELETE CASCADE
- 'id_objednavatel' - ON DELETE CASCADE


## Indexy - /sql/indexes.sql
- Databáze má pro každou entitu pouze indexy vytvořené pro primární klíče, 
  a další indexy 	- u entity objednatel - index_objednavatel na základě atributů jmeno_nazev_firmy,prijmeni
			- u entity misto_prace - index_misto_prace na základě atributů obec,cislo_popisne
			- u entity druh_prace - index_druh_prace na základě atributu druh

## Pohledy -  /sql/views.sql
- Návrh obsahuje pohledy na zobrazení místa práce a dotčených míst u tohoto místa , všech žádostí(jméno/firma objednavatele, případně příjmení, adresa, datum potvrzeni)

## Triggery - /sql/triggers.sql
- Databáze obsahuje triggery 	- pro kontrolu emailu u tabulky objednavatel, zda-li odpovídá formátu emailu
				- pro kontrolu dic u tabulky objednavatel, zda-li odpovídá formátu dič
				- pro kontrolu ico u tabulky objednavatel, zda-li odpovídá formátu ičo
				- pro kontrolu katastralni_uzemi u tabulky misto_prace, zda-li odpovídá formátu kódu katastrálního území

## Uložené procedury a funkce - /sql/procedures.sql
- Databáze obsahuje procedury 	- pro vypsání všech poptávek od daného objednavatele na základě jeho jména/ názvu firmy, případně příjmení a emailu
				- pro přidání objednavatele
				- pro přidání místa práce
				- pro vypsání objednávek podle roku potvrzení

## Přístupové údaje do databáze - /sql/users.sql
př:
- Přístupové údaje jsou volně konfigurovatelné v souboru /config/login.conf
pro vývoj byly použity tyto:

zadavac_objednavek
host		: localhost
uživatel	: zadavac_objednavek
heslo		: 123
databáze	: vodohospodarstvi

zadavac_sousedu
host		: localhost
uživatel	: zadavac_sousedu
heslo		: 123
databáze	: vodohospodarstvi

zadavac_objednavek
host		: localhost
uživatel	: manazer
heslo		: 123
databáze	: vodohospodarstvi

## Import struktury databáze a dat od zadavatele
př:
Nejprve je nutno si vytvořit novou databázi, čistou, bez jakýchkoliv dat...
Poté do této databáze nahrát soubory, které se nachází v /sql/structure.sql,views.sql,procedures.sql,triggers.sql,users.sql,indexes.sql
Pokud si přejete načíst do databáze testovací data, je nutno nahrát ještě každý soubor ze složky /sql/testovaci_data

## Export struktury databáze

- rozdilovy(kazdy tyden) - Server -> Data Export -> vybrat vsechny tabulky -> objects to export odkliknout vsechny -> Export to Dump Project Folder a vybrat misto -> Start Export
- plny(kazdy mesic) - Server -> Data Export -> vybrat databazi -> objects to export odkliknout vsechny -> Export to Self-Contained File -> zakliknout Create Dump in Single Transaction a Include Create Schema -> Start Export

## Klientská aplikace
- Databáze neobsahuje klientskou aplikaci, jelikož není součástí zadání

## Požadavky na spuštění
- MYSQL Workbench, MYSQL server lokální nebo online
- stabilní připojení k internetu alespoň 2Mb/s ...


## Návod na instalaci a ovládání aplikace
př:
Uživatel by si měl vytvořit databázi a nahrát do ní strukturu, dle kroku "Import struktury databáze 
a dat od zadavatele" ...
Poté se přihlásit předdefinovaným uživatelem, nebo si vytvořit vlastního pomocí SQL příkazů ...
Měl by upravit konfigurační soubor klientské aplikace, aby odpovídal jeho podmínkám ...
Dále nahrát obsah složky src na server a navštívit adresu serveru ... 
Přihlásit se a může začít pracovat ... 

## Závěr
př:
Tento systém by po menších úpravách mohl být převeden na jiný databázový systém, počítá se s tím, že každý, kdo bude přistupovat k databázi bude proškolen o používání této databáze. Je možné vyčlenit adresu z objednavatele a mista_prace do samostatne tabulky, ale to mi prislo zbytecne.
Export nebylo možné provést, jelikož mám jinou verzi MySQL Workbench a lokálního serveru viz. img/chyba.png. Řešením toho by bylo si naistalovat stejné verze serveru i MySQL Workbench