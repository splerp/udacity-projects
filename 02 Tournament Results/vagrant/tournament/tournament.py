#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


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


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM player")

    return c.rowcount


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO player (name, imagesDirectory) values (%s,'img/player/1')"
    data = (name, )
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()


def playerStandings():
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
    
    playerStandingsList = []
    
    # For each player, find the matches they played in.
    for id, name in allPlayers:
        print("FOund a player: " + str(id) + " - " + name)
        
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

















