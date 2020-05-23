SHOW DATABASES;
USE statbotics;

SHOW TABLES;
SELECT * FROM rankings_teammatch LIMIT 1000000;
SELECT * FROM rankings_teamevent LIMIT 100000;
SELECT * FROM rankings_teamyear LIMIT 100000;
SELECT * FROM rankings_team LIMIT 10000;
SELECT * FROM rankings_event LIMIT 10000;
SELECT * FROM rankings_year LIMIT 100;

DROP TABLE rankings_teammatch;
DROP TABLE rankings_teamevent;
DROP TABLE rankings_teamyear;
DROP TABLE rankings_team;
DROP TABLE rankings_event;
DROP TABLE rankings_year;

SELECT * FROM rankings_teamevent WHERE team=5511;
