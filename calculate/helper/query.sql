CREATE DATABASE IF NOT EXISTS statbotics;
USE statbotics;
SHOW TABLES;

# get head of tables
SELECT * FROM teams LIMIT 10000000;
SELECT * FROM years LIMIT 10000000;
SELECT * FROM team_years LIMIT 10000000;
SELECT * FROM events LIMIT 10000000;
SELECT * FROM team_events LIMIT 10000000;
SELECT * FROM matches LIMIT 10000000;
SELECT * FROM team_matches LIMIT 100000000;

SELECT COUNT(*) FROM matches;
SELECT COUNT(*) FROM team_matches;
SELECT SUM(elo_mse)/COUNT(elo_mse), SUM(opr_mse)/COUNT(opr_mse), SUM(mix_mse)/COUNT(mix_mse) FROM years WHERE id >= 2010;
SELECT SUM(elo_acc)/COUNT(elo_acc), SUM(opr_acc)/COUNT(opr_mse), SUM(mix_acc)/COUNT(mix_acc) FROM years WHERE id >= 2010;

# To restart process.py at a specific year
DELETE FROM team_years WHERE year_id=2020;
DELETE FROM years WHERE id=2020;

# Migrations
ALTER TABLE team_events ADD ils_2_end FLOAT;

DROP TABLE association3;

# Create a backup
CREATE DATABASE statbotics_backup;
CREATE TABLE statbotics_backup.teams select * from statbotics.teams;
CREATE TABLE statbotics_backup.years select * from statbotics.years;
CREATE TABLE statbotics_backup.team_years select * from statbotics.team_years;
CREATE TABLE statbotics_backup.events select * from statbotics.events;
CREATE TABLE statbotics_backup.team_events select * from statbotics.team_events;
CREATE TABLE statbotics_backup.matches select * from statbotics.matches;
CREATE TABLE statbotics_backup.team_matches select * from statbotics.team_matches;
