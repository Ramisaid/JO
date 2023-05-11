-- TODO 3.3 Créer un trigger pertinent
CREATE TRIGGER aft_update AFTER UPDATE ON LesResultats
BEGIN
INSERT into logs (id,numEp,datemaj) values(null,OLD.numEp,DATE('now'));
END;