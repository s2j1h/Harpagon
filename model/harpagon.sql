CREATE TABLE transactions (id integer primary key, dated date, ref1 text, ref2 text, value real,comment text,categoryID integer);
CREATE TABLE categories (id integer primary key, category text);
CREATE TABLE searchStrings (id integer primary key, searchString text, categoryID integer);

"""aucune est obligatoire"""

INSERT INTO categories (category) values ("aucune");
INSERT INTO categories (category) values ("Courses");
INSERT INTO categories (category) values ("Emploi à Domicile");

"""POUR LES TESTS"""

INSERT INTO searchStrings(searchString,categoryID) values ("MONOPRIX","2");
INSERT INTO searchStrings(searchString,categoryID) values ("PAJEMPLOI","3");
INSERT INTO searchStrings(searchString,categoryID) values ("GILLET","2");
INSERT INTO searchStrings(searchString,categoryID) values ("G 20","2");

"""SUPPRIMER COLONNE"""

BEGIN TRANSACTION;
CREATE TEMPORARY TABLE transactions_backup (id integer primary key, dated date, ref1 text, value real,comment text,categoryID integer);
INSERT INTO transactions_backup SELECT id,dated,ref1,value,comment,categoryID FROM transactions;
DROP TABLE transactions;
CREATE TABLE transactions (id integer primary key, dated date, ref1 text, value real,comment text,categoryID integer);
INSERT INTO transactions SELECT id,dated,ref1,value,comment,categoryID FROM transactions_backup;
DROP TABLE transactions_backup;
COMMIT;
