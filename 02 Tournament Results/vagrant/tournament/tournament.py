#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


'''
deleteMatches(tournID)
deletePlayers(tournID) - remove the tournamentPlayers for this tournament
countPlayers(tournID) - all players in a particular tournament
registerPlayer(tournID) - add tournamentPlayers for this tournament
playerStandings(tournID)
reportMatch(tournID, winner, loser)
swissPairings(tournID)
'''

def playMatch(tournID, p1ID, p2ID, matchResult):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO tournamentMatch (tournamentID, tournamentPlayer1ID, tournamentPlayer2ID, matchResult) VALUES (%s, %s, %s, %s)"
    data = (tournID, p1ID, p2ID, matchResult)
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()
    

def clearAllData():
    
    conn = connect()
    c = conn.cursor()
    
    #c.execute("TRUNCATE player CASCADE")
    #c.execute("TRUNCATE tournament CASCADE")
    c.execute("TRUNCATE tournamentMatch CASCADE")
    c.execute("TRUNCATE tournamentPlayer CASCADE")
    
    conn.commit()
    conn.close()
    
    

def addNewTournament(name):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO tournament (tournamentName) values (%s)"
    data = (name, )
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()
    
    

# Creates a new player for use in the system.
def addNewPlayer(name, age, gender, nationality):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO player (playerName, age, gender, nationality) values (%s, %s, %s, %s)"
    data = (name, age, gender, nationality)
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()

def removePlayer(name):

    conn = connect()
    c = conn.cursor()
    
    SQL = "DELETE FROM player WHERE playerName=%s;"
    data = (name)
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournaments")


def deleteMatches():
    """Remove all the match records from the database."""
    
    conn = connect()
    c = conn.cursor()
    
    c.execute("TRUNCATE tournamentMatch")
    
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    
    conn = connect()
    c = conn.cursor()
    
    c.execute("TRUNCATE player CASCADE")
    
    conn.commit()
    conn.close()

def getPlayerIDFromName(name):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "SELECT playerID FROM player WHERE playerName=%s"
    data = (name, )
    c.execute(SQL, data)
    
    toReturn = c.fetchone()
    
    conn.commit()
    conn.close()
    
    
    print("Searched for playerID. Got: " + str(toReturn) + ".")
    return toReturn[0]

    
def getTournamentIDFromName(name):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "SELECT tournamentID FROM tournament WHERE tournamentName=%s"
    data = (name, )
    c.execute(SQL, data)
    
    toReturn = c.fetchone()
    
    conn.commit()
    conn.close()
    
    
    print("Searched for tournID. Got: " + str(toReturn) + ".")
    return toReturn[0]

def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM player")

    return c.rowcount


def registerPlayer(tournID, playerID):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    # First: If this player does not exist, add them to the Player table.
    # Then, continue and add a tournamentPlayer entry.
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO tournamentPlayer (tournamentID, playerID) values (%s,%s)"
    data = (tournID, playerID)
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()

def playerRankingsView(tournID):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = """
    SELECT player.playerID, player.playerName, sum(NumGames) AS GamesPlayed, sum(Points) AS TotalPoints
    FROM
    player INNER JOIN 
    (
    SELECT tournamentMatch.tournamentID, tournamentPlayer1ID AS playerID, playerName, SUM(pointValue1) AS Points, count(*) AS NumGames
        FROM tournamentMatch 
        LEFT JOIN tournamentPlayer ON tournamentPlayer.playerID = tournamentMatch.tournamentPlayer1ID
        LEFT JOIN player ON tournamentPlayer.playerID = player.playerID
        INNER JOIN swissResult ON tournamentMatch.matchResult = swissResult.description
        WHERE tournamentMatch.tournamentID = %s
        GROUP BY tournamentPlayer1ID, tournamentMatch.tournamentID, player.playerName
    UNION
    SELECT tournamentMatch.tournamentID, tournamentPlayer2ID, playerName, SUM(pointValue2), count(*) AS NumGames
        FROM tournamentMatch
        LEFT JOIN tournamentPlayer ON tournamentPlayer.playerID = tournamentMatch.tournamentPlayer2ID
        LEFT JOIN player ON tournamentPlayer.playerID = player.playerID
        INNER JOIN swissResult ON tournamentMatch.matchResult = swissResult.description
        WHERE tournamentMatch.tournamentID = %s
        GROUP BY tournamentPlayer2ID, tournamentMatch.tournamentID, player.playerName

    ) AS innersql
    ON innersql.playerID = player.playerID
    GROUP BY innersql.playerID, player.playerID;
    """
    data = (tournID, tournID)
    c.execute(SQL, data)
    
    allResults = c.fetchall()
    return allResults
    
    
def playerStandings(tournID):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    
    print("\n\nGetting player standings...")
    
    # Open DB.
    conn = connect()
    c = conn.cursor()
    
    # Get each player's details.
    c.execute("SELECT playerID, name from player;")
    allPlayers = c.fetchall()
    
    SQL = "SELECT playerID, tournamentID, player.name, tournament.name "
    "FROM tournamentPlayer "
    "INNER JOIN player ON player.playerID = tournamentPlayer.playerID "
    "INNER JOIN tournament ON tournament.tournamentID = tournamentPlayer.tournamentID "
    "ORDER BY tournamentID, player.name;"
    
    playerStandingsList = []
    
    # For each player, find the matches they played in.
    for id, name in allPlayers:
        print("Found a player: " + str(id) + " - " + name)
        
        # Get total matches played
        SQL = "SELECT * FROM tournamentMatch WHERE playerWinnerID = %s OR playerLoserID = %s;"
        data = (id, id)
        c.execute(SQL, data)
        totalMatches = c.rowcount
        
        # Get total matches won
        SQL = "SELECT * FROM tournamentMatch WHERE playerWinnerID = %s;"
        data = (id, )
        c.execute(SQL, data)
        wonMatches = c.rowcount
        
         # Add new tuple to player list.
        playerStandingsList.append((id, name, wonMatches, totalMatches))
    
    print("returning " + str(playerStandingsList))
    return playerStandingsList

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO tournamentMatch (playerWinnerID, playerLoserID) values (%s, %s)"
    data = (winner, loser)
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    playerStandingsList = playerStandings()
    sortedPlayers = sorted(playerStandingsList, key=lambda player: player[2]) # sort by num wins
    
    print("\n\n Getting Swiss pairs...")
    
    # Open DB.
    conn = connect()
    c = conn.cursor()
    
    # Get each player's details.
    c.execute("SELECT playerID, name from player;")
    allPlayers = c.fetchall()
    
    swissPairingsList = []
    
    totalPlayers = c.rowcount
    print("Total players: " + str(totalPlayers))
    
    i = 0
    while i < totalPlayers:
        
        p1 = sortedPlayers[i]
        p2 = sortedPlayers[i+1]
        
        swissPairingsList.append((p1[0], p1[1], p2[0], p2[1]))
        
        i += 2
    
    # Get all existing players (Sort by number of wins).
    
    # Pair the first two up, then the next two, etc.
    
    # return the new list (id1, name1, id2, name2)
    print("returning " + str(swissPairingsList))
    return swissPairingsList

















