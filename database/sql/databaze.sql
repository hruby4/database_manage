SET autocommit = off;
START TRANSACTION;

create database vodohospodarstvi;
use vodohospodarstvi;

create table pozemek(
cislo int primary key not null unique
);

create table misto_prace(
id int primary key auto_increment not null unique,
obec varchar(40) not null,
ulice varchar(40) not null,
cislo_popisne int not null,
katastralni_uzemi varchar(6) not null,
cast_mesta ENUM('Sever','Jih','Zapad','Vychod')
);

create table sousedstvi(
id int primary key auto_increment not null unique,
id_pozemek int not null,
id_misto_prace int not null,
FOREIGN KEY (id_pozemek) REFERENCES pozemek(cislo)
ON DELETE CASCADE,
FOREIGN KEY (id_misto_prace) REFERENCES misto_prace(id)
ON DELETE CASCADE
);

create table druh_prace(
id int primary key auto_increment not null unique,
druh varchar(60) not null,
obtiznost FLOAT NOT NULL
);


create table objednavatel(
id int primary key auto_increment not null unique,
jmeno_nazev_firmy varchar(20) not null,
prijmeni varchar(20),
ulice varchar(40) not null,
cislo_popisne int not null,
mesto varchar(40) not null,
psc varchar(5) not null,
CHECK (psc>=10000 and psc <= 99999),
ico varchar(8) unique,
dic varchar(10) unique,
telefon int not null unique,
CHECK (telefon>=100000000 and telefon <= 999999999),
fax int not null,
email varchar(319) unique,
platce_dph boolean not null
);

create table objednavka(
id int primary key auto_increment not null unique,
id_druh_prace int not null,
id_objednavatel int not null,
id_misto_prace int not null,
FOREIGN KEY (id_misto_prace) REFERENCES misto_prace(id)
ON DELETE CASCADE,
FOREIGN KEY (id_druh_prace) REFERENCES druh_prace(id)
ON DELETE CASCADE,
FOREIGN KEY (id_objednavatel) REFERENCES objednavatel(id)
ON DELETE CASCADE,
souvisi_zakon boolean not null,
souvisi_ekonomicka_cinnost boolean not null,
zprac_osobni_udaje boolean not null,
datum_potvrzeni date not null,
check (datum_potvrzeni <= SYSDATE()),
misto_potvrzeni varchar(40) not null

);

CREATE INDEX index_objednavatel
ON objednavatel (jmeno_nazev_firmy,prijmeni);


CREATE INDEX index_misto_prace
ON misto_prace (obec,cislo_popisne);

CREATE INDEX index_druh_prace
ON druh_prace (druh);


create view vypis_zadosti as
select druh_prace.druh,objednavatel.jmeno_nazev_firmy,objednavatel.prijmeni,misto_prace.obec,misto_prace.ulice,misto_prace.cislo_popisne,misto_prace.katastralni_uzemi,objednavka.datum_potvrzeni
from objednavka
inner join objednavatel on objednavka.id_objednavatel = objednavatel.id
inner join druh_prace on druh_prace.id = objednavka.id_druh_prace
inner join misto_prace on misto_prace.id = objednavka.id_misto_prace;

select * from vypis_zadosti;



create view vypis_sousedu as
select misto_prace.obec,misto_prace.cislo_popisne,pozemek.cislo from sousedstvi
inner join misto_prace on misto_prace.id = sousedstvi.id_misto_prace
inner join pozemek on pozemek.cislo = sousedstvi.id_pozemek
group by misto_prace.cislo_popisne;

select * from vypis_sousedu;


CREATE USER 'zadavac_objednavek'@'localhost' IDENTIFIED BY '123';
CREATE USER 'zadavac_sousedu'@'localhost' IDENTIFIED BY '123';
CREATE USER 'manazer'@'localhost' IDENTIFIED BY '123';



GRANT ALL PRIVILEGES ON vodohospodarstvi.* TO 'manazer'@'localhost' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON vodohospodarstvi.pozemek TO 'zadavac_sousedu'@'localhost';
GRANT ALL PRIVILEGES ON vodohospodarstvi.sousedstvi TO 'zadavac_sousedu'@'localhost';
GRANT ALL PRIVILEGES ON vodohospodarstvi.objednavka TO 'zadavac_objednavek'@'localhost';
GRANT ALL PRIVILEGES ON vodohospodarstvi.misto_prace TO 'zadavac_objednavek'@'localhost';
GRANT ALL PRIVILEGES ON vodohospodarstvi.objednavatel TO 'zadavac_objednavek'@'localhost';
FLUSH PRIVILEGES;

DELIMITER //

CREATE PROCEDURE VypisVsechnyObjednavkyObjednavatele(jmeno varchar(20),prijmeni varchar(40),email varchar(319))
BEGIN
	select objednavatel.jmeno_nazev_firmy,objednavatel.prijmeni,misto_prace.obec,misto_prace.ulice,misto_prace.cislo_popisne,misto_prace.katastralni_uzemi,objednavka.datum_potvrzeni
	from objednavka
	inner join objednavatel on objednavka.id_objednavatel = objednavatel.id
	inner join druh_prace on objednavka.id_druh_prace = druh_prace.id
	inner join misto_prace on misto_prace.id = objednavka.id_misto_prace
    where objednavatel.jmeno_nazev_firmy = jmeno and objednavatel.prijmeni = prijmeni and objednavatel.email = email;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE PridejObjednavatele(jmeno_nazev_firmy varchar(20),prijmeni varchar(40),ulice varchar(40),cislo_popisne int,mesto varchar(40),psc varchar(5),ico int,dic varchar(10),telefon int, fax int ,email varchar(319),platce_dph boolean)
BEGIN
	insert into objednavatel(jmeno_nazev_firmy,prijmeni,ulice,cislo_popisne,mesto,psc,ico,dic,telefon,fax,email,platce_dph) values(jmeno_nazev_firmy,prijmeni,ulice,cislo_popisne,mesto,psc,ico,dic,telefon,fax,email,platce_dph);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE PridejMistoPrace(obec varchar(40),ulice varchar(40),cislo_popisne int,katastralni_uzemi varchar(6))
BEGIN
	insert into misto_prace(obec,ulice,cislo_popisne,katastralni_uzemi) values(obec,ulice,cislo_popisne,katastralni_uzemi);
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE PridejObjednavku(druh_prace varchar(60), email varchar(319), obec varchar(40),cislo_popisne int,souvisi_zakon boolean, souvisi_ekonomicka_cinnost boolean,zprac_osobni_udaje boolean, datum_potvrzeni date, misto_potvrzeni varchar(40))
BEGIN
	DECLARE id_objednavatel, id_misto_prace,id_druh_prace INT DEFAULT 0;
    select id from objednavatel where objednavatel.email = email
    into id_objednavatel;
    select id from misto_prace where misto_prace.cislo_popisne = cislo_popisne and misto_prace.obec = obec
    into id_misto_prace;
    select id from druh_prace where druh_prace.druh = druh_prace
    into id_druh_prace;
	insert into objednavka (id_druh_prace, id_objednavatel, id_misto_prace, souvisi_zakon, souvisi_ekonomicka_cinnost, zprac_osobni_udaje, datum_potvrzeni, misto_potvrzeni) values (id_druh_prace, id_objednavatel, id_misto_prace, souvisi_zakon, souvisi_ekonomicka_cinnost, zprac_osobni_udaje, datum_potvrzeni, misto_potvrzeni);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE VypisVsechnyObjednavkyPodleRoku(rok int)
BEGIN
	select objednavatel.jmeno_nazev_firmy,objednavatel.prijmeni,misto_prace.obec,misto_prace.ulice,misto_prace.cislo_popisne,misto_prace.katastralni_uzemi,objednavka.datum_potvrzeni
	from objednavka
	inner join objednavatel on objednavka.id_objednavatel = objednavatel.id
	inner join druh_prace on objednavka.id_druh_prace = druh_prace.id
	inner join misto_prace on misto_prace.id = objednavka.id_misto_prace
    where YEAR(objednavka.datum_potvrzeni) = rok;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER emailCheck BEFORE INSERT ON objednavatel
FOR EACH ROW
BEGIN
IF (NEW.email REGEXP '^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9._-]@[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]\\.[a-zA-Z]{2,63}$' ) = 0 THEN
-- ROLLBACK;
SIGNAL SQLSTATE '33455'
SET MESSAGE_TEXT = 'Format emailu je spatny';
END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER dicCheck BEFORE INSERT ON objednavatel
FOR EACH ROW
BEGIN
IF (NEW.dic REGEXP '^[A-Z]{2}[0-9]{8,10}$' ) = 0 THEN
-- ROLLBACK;
SIGNAL SQLSTATE '33455'
SET MESSAGE_TEXT = 'Format DIC je spatny';
END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER icoCheck BEFORE INSERT ON objednavatel
FOR EACH ROW
BEGIN
IF (NEW.ico REGEXP '^[0-9]{8,10}$' ) = 0 THEN
-- ROLLBACK;
SIGNAL SQLSTATE '33455'
SET MESSAGE_TEXT = 'Format ICO je spatny';
END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER katastralni_uzemiCheck BEFORE INSERT ON misto_prace
FOR EACH ROW
BEGIN
IF (NEW.katastralni_uzemi REGEXP '^[0-9]{6}$' ) = 0 THEN
-- ROLLBACK;
SIGNAL SQLSTATE '33455'
SET MESSAGE_TEXT = 'Format ICO je spatny';
END IF;
END //

DELIMITER ;



COMMIT;
