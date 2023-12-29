set autocommit= off;

START transaction;

insert into druh_prace(druh)values
('Zhotovení nové vodovodní nebo kanalizační připojky'), ('Oprava stávající vodovodní nebo kanalizační přípojky'),('Výměna poškozeného vodoměru,Osazení vodoměru'),('Jiné práce a služby');
commit;