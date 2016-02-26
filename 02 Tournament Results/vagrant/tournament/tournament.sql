-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Remove all previous instances.
DROP TABLE IF EXISTS tournamentMatch;
DROP TABLE IF EXISTS tournamentPlayer;
DROP TABLE IF EXISTS tournament;
DROP TABLE IF EXISTS player;

DROP TABLE IF EXISTS swissResult;


CREATE TABLE tournament (
tournamentID serial PRIMARY KEY,
tournamentName varchar(50) UNIQUE NOT NULL,
dateCreated timestamp DEFAULT current_timestamp,
imagesDirectory varchar(50));

--

CREATE TABLE player (
playerID serial PRIMARY KEY,
playerName varchar(50) UNIQUE NOT NULL,
age int,
gender varchar(1),
nationality varchar(3),
imagesDirectory varchar(50));

--

CREATE TABLE tournamentPlayer (
tournamentPlayerID serial PRIMARY KEY,
tournamentID int REFERENCES tournament (tournamentID),
playerID int REFERENCES player (playerID)
);

--

CREATE TABLE swissResult (
description varchar(20) PRIMARY KEY,
pointValue1 int,
pointValue2 int
);

--

CREATE TABLE tournamentMatch (
tournamentMatchID serial PRIMARY KEY,
tournamentID int REFERENCES tournament (tournamentID),
tournamentPlayer1ID int REFERENCES player (playerID),
tournamentPlayer2ID int REFERENCES player (playerID),
matchResult varchar(20) REFERENCES swissResult(description), 
datePlayed timestamp DEFAULT current_timestamp
);


INSERT INTO swissResult (description, pointValue1, pointValue2)
values
('p1 wins', 3, 0),
('p2 wins', 0, 3),
('draw', 1, 1),
('cancelled', 0, 0)
;


