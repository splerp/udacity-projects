-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP VIEW IF EXISTS playerTotalInfo;
DROP VIEW IF EXISTS playerAllTournsInfo;

DROP VIEW IF EXISTS opponentMatchWins;
DROP VIEW IF EXISTS playerOpponents;

DROP VIEW IF EXISTS individualTournamentPlayerWins;
DROP VIEW IF EXISTS individualTournamentPlayerDraws;
DROP VIEW IF EXISTS individualTournamentPlayerLosses;
DROP VIEW IF EXISTS individualTournamentPlayerGamesPlayed;


-- Remove all previous instances.
DROP TABLE IF EXISTS tournamentMatch;
DROP TABLE IF EXISTS tournamentPlayer;
DROP TABLE IF EXISTS tournament;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS swissResult;


CREATE TABLE tournament (
tournamentID serial PRIMARY KEY,
tournamentName varchar(50) UNIQUE NOT NULL,
dateCreated timestamp DEFAULT current_timestamp);

--

CREATE TABLE player (
playerID serial PRIMARY KEY,
playerName varchar(50) UNIQUE NOT NULL,
age int,
gender varchar(1),
nationality varchar(3));

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
tournamentPlayer1ID int REFERENCES tournamentPlayer (tournamentPlayerID),
tournamentPlayer2ID int REFERENCES tournamentPlayer (tournamentPlayerID),
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

-- Wins view
CREATE VIEW individualTournamentPlayerWins AS
SELECT tmp.tournamentID, player.playerID, sum(total) AS winTotal FROM
(
SELECT tournamentID, tournamentPlayer1ID AS tournamentPlayerID, count(matchResult) AS total
	FROM tournamentMatch
	
	WHERE tournamentMatch.matchResult='p1 wins'
	GROUP BY tournamentPlayer1ID, tournamentID
UNION ALL
SELECT tournamentID, tournamentPlayer2ID AS tournamentPlayerID, count(matchResult) AS total
	FROM tournamentMatch
	
	WHERE tournamentMatch.matchResult='p2 wins'
	GROUP BY tournamentPlayer2ID, tournamentID
	
) as tmp
INNER JOIN tournamentPlayer ON tournamentPlayer.tournamentPlayerID = tmp.tournamentPlayerID
INNER JOIN player ON player.playerID = tournamentPlayer.playerID
GROUP BY player.playerID, tmp.tournamentID
;

-- Losses view
CREATE VIEW individualTournamentPlayerLosses AS
SELECT tmp.tournamentID, player.playerID, sum(total) AS loseTotal FROM
(
SELECT tournamentID, tournamentPlayer1ID AS tournamentPlayerID, count(matchResult) AS total
	FROM tournamentMatch
	
	WHERE tournamentMatch.matchResult='p2 wins'
	GROUP BY tournamentPlayer1ID, tournamentID
UNION ALL
SELECT tournamentID, tournamentPlayer2ID AS tournamentPlayerID, count(matchResult) AS total
	FROM tournamentMatch
	
	WHERE tournamentMatch.matchResult='p1 wins'
	GROUP BY tournamentPlayer2ID, tournamentID
	
) as tmp
INNER JOIN tournamentPlayer ON tournamentPlayer.tournamentPlayerID = tmp.tournamentPlayerID
INNER JOIN player ON player.playerID = tournamentPlayer.playerID
GROUP BY player.playerID, tmp.tournamentID
;

-- Draws view
CREATE VIEW individualTournamentPlayerDraws AS
SELECT tmp.tournamentID, player.playerID, sum(total) AS drawTotal FROM
(
SELECT tournamentID, tournamentPlayer1ID AS tournamentPlayerID, count(matchResult) AS total
	FROM tournamentMatch
	
	WHERE tournamentMatch.matchResult='draw'
	GROUP BY tournamentPlayer1ID, tournamentID
UNION ALL
SELECT tournamentID, tournamentPlayer2ID AS tournamentPlayerID, count(matchResult) AS total
	FROM tournamentMatch
	
	WHERE tournamentMatch.matchResult='draw'
	GROUP BY tournamentPlayer2ID, tournamentID
	
) as tmp
INNER JOIN tournamentPlayer ON tournamentPlayer.tournamentPlayerID = tmp.tournamentPlayerID
INNER JOIN player ON player.playerID = tournamentPlayer.playerID
GROUP BY player.playerID, tmp.tournamentID
;

-- Total games played view
CREATE VIEW individualTournamentPlayerGamesPlayed AS
SELECT tmp.tournamentID, player.playerID, sum(total) AS totalGames FROM
(
SELECT tournamentID, tournamentPlayer1ID AS tournamentPlayerID, count(matchResult) AS total
	FROM tournamentMatch
	GROUP BY tournamentPlayer1ID, tournamentID
UNION ALL
SELECT tournamentID, tournamentPlayer2ID AS tournamentPlayerID, count(matchResult) AS total
	FROM tournamentMatch
	GROUP BY tournamentPlayer2ID, tournamentID
	
) as tmp
INNER JOIN tournamentPlayer ON tournamentPlayer.tournamentPlayerID = tmp.tournamentPlayerID
INNER JOIN player ON player.playerID = tournamentPlayer.playerID
GROUP BY player.playerID, tmp.tournamentID
;

CREATE VIEW playerOpponents AS
SELECT player.playerID, tmp.tournamentID, tmp.tournamentPlayerID, tmp.opponentTournamentPlayerID FROM
(
	SELECT tournamentID, tournamentPlayer2ID AS tournamentPlayerID, tournamentPlayer1ID as opponentTournamentPlayerID FROM tournamentMatch
	UNION ALL
	SELECT tournamentID, tournamentPlayer1ID AS tournamentPlayerID, tournamentPlayer2ID as opponentTournamentPlayerID FROM tournamentMatch
) as tmp
INNER JOIN tournamentPlayer ON tournamentPlayer.tournamentPlayerID = tmp.tournamentPlayerID
INNER JOIN player ON player.playerID = tournamentPlayer.playerID
GROUP BY tmp.tournamentPlayerID, tmp.tournamentID, tmp.opponentTournamentPlayerID, player.playerID
ORDER BY tmp.tournamentID, tmp.tournamentPlayerID
;

CREATE VIEW opponentMatchWins AS
SELECT tournamentPlayer.tournamentID, tournamentPlayer.playerID, SUM(COALESCE(wins, 0)) as opponentTotalWins FROM playerOpponents 
LEFT JOIN tournamentPlayer ON playerOpponents.opponentTournamentPlayerID = tournamentPlayer.tournamentPlayerID 
LEFT JOIN 
(
	SELECT playerID, tournamentID, winTotal as wins
	FROM individualTournamentPlayerWins
) as tmp2
ON tmp2.playerID = playerOpponents.playerID
AND tmp2.tournamentID = playerOpponents.tournamentID
GROUP BY tournamentPlayer.tournamentID, tournamentPlayer.playerID
ORDER BY tournamentPlayer.tournamentID, tournamentPlayer.playerID
;

-- Combination of player details, and the game stats (wins, losses etc.)
CREATE VIEW playerAllTournsInfo AS 
SELECT player.playerID, player.playerName, player.age, player.gender, player.nationality, tournamentPlayer.tournamentID, 
	sum(COALESCE(winTotal, 0)) as wins, sum(COALESCE(drawTotal, 0)) as draws, sum(COALESCE(loseTotal, 0)) as losses, sum(COALESCE(totalGames, 0)) as totalGames, sum(COALESCE(opponentTotalWins, 0)) as opponentMatchWins
FROM player 
INNER JOIN tournamentPlayer 
    ON player.playerID = tournamentPlayer.playerID 
LEFT JOIN individualTournamentPlayerWins 
    ON tournamentPlayer.tournamentID = individualTournamentPlayerWins.tournamentID 
    AND player.playerID = individualTournamentPlayerWins.playerID 
LEFT JOIN individualTournamentPlayerDraws
    ON tournamentPlayer.tournamentID = individualTournamentPlayerDraws.tournamentID 
    AND player.playerID = individualTournamentPlayerDraws.playerID 
LEFT JOIN individualTournamentPlayerLosses 
    ON tournamentPlayer.tournamentID = individualTournamentPlayerLosses.tournamentID 
    AND player.playerID = individualTournamentPlayerLosses.playerID 
LEFT JOIN individualTournamentPlayerGamesPlayed 
    ON tournamentPlayer.tournamentID = individualTournamentPlayerGamesPlayed.tournamentID 
    AND player.playerID = individualTournamentPlayerGamesPlayed.playerID 
LEFT JOIN opponentMatchWins 
    ON tournamentPlayer.tournamentID = opponentMatchWins.tournamentID 
    AND player.playerID = opponentMatchWins.playerID 
GROUP BY player.playerID, tournamentPlayer.tournamentID
ORDER BY tournamentPlayer.tournamentID, player.playerID
;

-- Gets a "grand total" view which combines the wins, losses etc. for all tournaments.
-- Do not SELECT tournamentID - want to combine columns where this value would be different.
CREATE VIEW playerTotalInfo AS 
SELECT playerID, playerName, age, gender, nationality,
	sum(wins) as wins, sum(draws) as draws, sum(losses) as losses, sum(totalGames) as totalGames
FROM playerAllTournsInfo 
GROUP BY playerID, playerName, age, gender, nationality;


