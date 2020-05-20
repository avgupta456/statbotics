SHOW DATABASES;
USE statbotics;

SHOW TABLES;
SELECT * FROM rankings_teammatch LIMIT 1000000;
SELECT * FROM rankings_teamevent LIMIT 100000;
SELECT * FROM rankings_teamyear LIMIT 100000;
SELECT * FROM rankings_team LIMIT 10000;
SELECT * FROM rankings_event LIMIT 10000;
SELECT * FROM rankings_year LIMIT 100;

TRUNCATE TABLE rankings_teammatch;
TRUNCATE TABLE rankings_teamevent;
TRUNCATE TABLE rankings_teamyear;
TRUNCATE TABLE rankings_team;
TRUNCATE TABLE rankings_event;
TRUNCATE TABLE rankings_year;
