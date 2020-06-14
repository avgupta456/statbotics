CREATE DATABASE IF NOT EXISTS statbotics;
USE statbotics;

SHOW TABLES;
SELECT * FROM teams;
SELECT * FROM years;
SELECT * FROM team_years;
SELECT * FROM events;
SELECT * FROM team_events;
SELECT * FROM matches;
SELECT COUNT(*) FROM team_matches;

DELETE FROM team_years WHERE year_id=2020;
DELETE FROM years WHERE id=2020;

ALTER TABLE teams ADD district VARCHAR(10);