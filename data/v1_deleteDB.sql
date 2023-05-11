-- TODO 1.3a : Détruire les tables manquantes et modifier celles ci-dessous
DROP TABLE IF EXISTS LesEpreuves;
DROP TABLE IF EXISTS LesEquipes;
DROP TABLE IF EXISTS LesSportifs;
DROP TABLE IF EXISTS LesInscriptions;
DROP TABLE IF EXISTS LesResultats;
DROP TABLE IF EXISTS logs;
DROP VIEW IF EXISTS LesAgesSportifs;
DROP VIEW IF EXISTS LesNbsEquipiers;
----------------------------------------
DROP VIEW IF EXISTS equipes_mixtes;
-- TODO 3.3 : pensez à détruire vos triggers !
DROP TRIGGER IF EXISTS aft_update;
