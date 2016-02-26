-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Remove all previous instances.
DROP TABLE IF EXISTS tournamentMatch;
DROP TABLE IF EXISTS tournament;
DROP TABLE IF EXISTS player;

--DROP DATABASE tournaments;


-- Update with new stuff.
--CREATE DATABASE tournaments;

CREATE TABLE tournament ( tournamentID serial PRIMARY KEY,
						name varchar(50) UNIQUE NOT NULL,
						dateCreated timestamp DEFAULT current_timestamp,
						imagesDirectory varchar(50));

CREATE TABLE player ( playerID serial PRIMARY KEY,
					name varchar(50) UNIQUE NOT NULL,
					imagesDirectory varchar(50));

CREATE TABLE tournamentMatch ( tournamentMatchID serial PRIMARY KEY,
							tournamentID int REFERENCES tournament (tournamentID),
							playerWinnerID int REFERENCES player (playerID),
							playerLoserID int REFERENCES player (playerID),
							datePlayed timestamp DEFAULT current_timestamp
							);
							
INSERT INTO tournament (name, imagesDirectory)
	values
	(
		'First Tourn',
		'images/asd'
	),
	(
		'Tournament 2',
		'images/asd'
	);

INSERT INTO player (name, imagesDirectory)
	values
	(
		'Player 1',
		'images/player/p1'
	),
	(
		'Best player',
		'images/player/p2'
	);

INSERT INTO tournamentMatch (tournamentID, playerWinnerID, playerLoserID)
	values
	(
		1,
		1,
		2
	),
	(
		1,
		1,
		2
	);



















