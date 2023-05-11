-- TODO 1.3a : Créer les tables manquantes et modifier celles ci-dessous
-- Les details de la BD finale seront disponible dans le COMPTE RENDU joint au projet
CREATE TABLE LesSportifs
(
  numSp NUMBER(4) NOT NULL,
  nomSp VARCHAR2(20) NOT NULL,
  prenomSp VARCHAR2(20) NOT NULL,
  pays VARCHAR2(20) NOT NULL,
  categorieSp VARCHAR2(20) NOT NULL,
  dateNaisSp DATE NOT NULL,
  CONSTRAINT LesSportifs_PRIMARYKEY PRIMARY KEY(numSp),
  CONSTRAINT LesSportifs_UNQ UNIQUE(nomSp, prenomSp),
  CONSTRAINT LesSportifs_CATCHECK CHECK((categorieSp =  'feminin' OR categorieSp =  'masculin')),
  CONSTRAINT LesSportifs_NUMCHECK CHECK(numSp >= 1000 AND  numSp <= 1500)
);


CREATE TABLE LesEquipes
(
  numEq NUMBER(4) NOT NULL,
  numSp NUMBER(4) NOT NULL,
  CONSTRAINT EQUIP_PRIMARYKEY PRIMARY KEY(numEq, numSp),
  CONSTRAINT EQUIP_NUMCHECK CHECK(numEq >= 1 AND numEq <= 100 ),
  CONSTRAINT EQUIP_FOREIGNYKEY FOREIGN KEY(numSp) REFERENCES LesSportifs(numSp)
);

CREATE TABLE LesEpreuves
(
  numEp NUMBER(4),
  nomEp VARCHAR2(20),
  formeEp VARCHAR2(13),
  nomDi VARCHAR2(20),
  categorieEp VARCHAR2(20),
  nbSportifsEp NUMBER(4),
  dateEp DATE,

  CONSTRAINT Epreuves_EQUIP_PRIMARYKEY PRIMARY KEY (numEp),
  CONSTRAINT Epreuves_CHECKNUMEP CHECK (numEp > 0),
  CONSTRAINT Epreuves_CHECKFORME CHECK ( formeEp = 'par couple' OR formeEp = 'individuelle' OR  formeEp = 'par equipe'),
  CONSTRAINT Epreuves_CHECKCATEGORIE CHECK (categorieEp = 'feminin' OR  categorieEp = 'masculin' OR categorieEp = 'mixte'),
  CONSTRAINT Epreuves_CHECKNBSP CHECK (nbSportifsEp > 0)
);

CREATE TABLE LesInscriptions
(
  numIn NUMBER(4) NOT NULL,
  numEp NUMBER(4) NOT NULL,
  CONSTRAINT INSCRIPTIONS_PRIMARYKEY PRIMARY KEY(numIn, numEp),
  CONSTRAINT INSCRIPTIONS_FOREIGNKEY FOREIGN KEY(numEp) REFERENCES LesEpreuves(numEp),
  CONSTRAINT INSCRIPTIONS_CHECK CHECK (numIn > 0)
);

CREATE TABLE LesResultats
(
  numEp NUMBER(4),
  gold NUMBER(4),
  silver NUMBER(4),
  bronze NUMBER(4),
  CONSTRAINT RESULTAT_PRIMARYKEY PRIMARY KEY (numEp),
  CONSTRAINT RESULTAT_FOREIGNYKEY1 FOREIGN KEY (gold, numEp) REFERENCES LesInscriptions(numIn,numEp),
  CONSTRAINT RESULTAT_FOREIGNYKEY2 FOREIGN KEY (silver, numEp) REFERENCES LesInscriptions(numIn,numEp),
  CONSTRAINT RESULTAT_FOREIGNYKEY3 FOREIGN KEY (bronze, numEp) REFERENCES LesInscriptions(numIn,numEp),
  CONSTRAINT RESULTAT_MEDAILLE1 CHECK (gold != silver AND gold > 0),
  CONSTRAINT RESULTAT_MEDAILLE2 CHECK (silver != bronze AND silver >0),
  CONSTRAINT RESULTAT_MEDAILLE3 CHECK (gold != bronze AND bronze > 0)
);

-- TODO 1.4a : ajouter la définition de la vue LesAgesSportifs
CREATE VIEW LesAgesSportifs(numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, ageSp) AS
    SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp,
        ((strftime('%Y', 'now') - strftime('%Y', dateNaisSp)) - (strftime('%m-%d', 'now') < strftime('%m-%d', dateNaisSp))) AS ageSp
    FROM LesSportifs;
-- TODO 1.5a : ajouter la définition de la vue LesNbsEquipiers
CREATE VIEW LesNbsEquipiers(numEq, nbEquipiersEq) AS
    SELECT numEq, COUNT(numSp) as nbEquipiersEq
    FROM LesEquipes
    WHERE numEq IS NOT NULL
    GROUP BY numEq ;


-------------- Vue Utilitaire pour la Partie 3.1 ---------------------------------------------------------------------
CREATE VIEW equipes_mixtes(numEq, categorieSp, nbSportifs) AS
    with equipes_masculine_feminine_2 as (
        SELECT E.numEq, E.numSp, SB."categorieSp" FROM LesEquipes E JOIN LesSportifs SB ON (SB.numSp = E.numSp) WHERE E.numEq IN (
            SELECT numEq FROM LesEquipes GROUP BY numEq having COUNT(numEq) = 2
        )
    )
    SELECT R1.numEq, "mixte" as categorieSp, 2 as nbSportifs FROM equipes_masculine_feminine_2 R1 JOIN equipes_masculine_feminine_2 R2 ON (R1.numEq=R2.numEq and R1.numSp != R2.numSp and R1.categorieSp != R2.categorieSp);

-- TODO 3.3 : ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)

CREATE TABLE logs
(
  id INTEGER,
  numEp NUMBER(4) NOT NULL,
  datemaj DATE,
  CONSTRAINT LOGS_PRIMARYKEY PRIMARY KEY(id)

);