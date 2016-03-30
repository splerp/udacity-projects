#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import argparse
import psycopg2

###
# PLAYERS
###

# Creates a new player for use in the system.
def addNewPlayer(name, age, gender, nationality):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO player (playerName, age, gender, nationality) values (%s, %s, %s, %s)"
    data = (name, age, gender, nationality)
    c.execute(SQL, data)
    conn.commit()

    SQL = "SELECT playerID FROM player WHERE playerName = %s"
    data = (name, )
    c.execute(SQL, data)

    newID = c.fetchone()
    newID = newID[0]

    conn.close()

    return newID

def removePlayer(name):

    conn = connect()
    c = conn.cursor()
    
    SQL = "DELETE FROM player WHERE playerName=%s;"
    data = (name, )
    c.execute(SQL, data)
    
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
    c.execute("SELECT count(*) FROM player")

    return c.fetchone()[0]

def getPlayerIDFromName(name):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "SELECT playerID FROM player WHERE playerName=%s"
    data = (name, )
    c.execute(SQL, data)
    
    toReturn = c.fetchone()
    
    conn.commit()
    conn.close()
    
    return toReturn[0]
    
def getPlayerTournID(tournID, playerID):
    
    theID = 0;
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "SELECT tournamentPlayerID FROM tournamentPlayer WHERE tournamentID = %s AND playerID = %s"
    data = (tournID, playerID)
    c.execute(SQL, data)
    
    theID = c.fetchone()
    
    conn.commit()
    conn.close()
    
    return theID

def registerPlayerByID(playerID, tournID):
    
    
    # First: If this player does not exist, add them to the Player table.
    # Then, continue and add a tournamentPlayer entry.
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO tournamentPlayer (tournamentID, playerID) values (%s,%s)"
    data = (tournID, playerID)
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()
    
def countPlayersInTournament(tournID):
    """Returns the number of tournaments currently registered."""

    conn = connect()
    c = conn.cursor()

    SQL = "SELECT count(*) FROM tournamentPlayer WHERE tournamentID = %s"
    data = (tournID,)
    c.execute(SQL, data)

    return c.fetchone()[0]

# Totals the wins of all the players this player has faced.
def getOpponentMatchWins(tournID, playerID):

    conn = connect()
    c = conn.cursor()

    SQL = "SELECT opponentTotalWins FROM opponentMatchWins WHERE tournamentID = %s AND playerID = %s"
    data = (tournID, playerID)
    c.execute(SQL, data)

    result = c.fetchone()
    
    return 0 if result is None else result[0]
    
    
###
# TOURNAMENTS
###

def addNewTournament(name):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO tournament (tournamentName) values (%s)"
    data = (name, )
    c.execute(SQL, data)
    conn.commit()

    SQL = "SELECT tournamentID FROM tournament WHERE tournamentName = %s"
    data = (name, )
    c.execute(SQL, data)

    newID = c.fetchone()
    newID = newID[0]

    conn.close()

    return newID

def getTournamentIDFromName(name):
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "SELECT tournamentID FROM tournament WHERE tournamentName=%s"
    data = (name, )
    c.execute(SQL, data)
    
    toReturn = c.fetchone()
    
    conn.commit()
    conn.close()
    
    return None if toReturn is None else toReturn[0]

def countTournaments():
    """Returns the number of tournaments currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM tournament")

    return c.fetchone()[0]
###
# MATCHES
###

def playMatch(tournID, p1ID, p2ID, matchResult):
    
    # Convert the player ID into a tournament player ID.
    pt1ID = getPlayerTournID(tournID, p1ID)
    pt2ID = getPlayerTournID(tournID, p2ID)
    
    conn = connect()
    c = conn.cursor()
    
    SQL = "INSERT INTO tournamentMatch (tournamentID, tournamentPlayer1ID, tournamentPlayer2ID, matchResult) VALUES (%s, %s, %s, %s)"
    data = (tournID, pt1ID, pt2ID, matchResult)
    c.execute(SQL, data)
    
    conn.commit()
    conn.close()

def deleteMatches():
    """Remove all the match records from the database."""
    
    conn = connect()
    c = conn.cursor()
    
    c.execute("TRUNCATE tournamentMatch")
    
    conn.commit()
    conn.close()
    
###
# OTHER
###
    
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournaments")

def clearAllData():
    
    conn = connect()
    c = conn.cursor()
    
    c.execute("TRUNCATE player CASCADE")
    c.execute("TRUNCATE tournament CASCADE")
    c.execute("TRUNCATE tournamentMatch CASCADE")
    c.execute("TRUNCATE tournamentPlayer CASCADE")
    
    conn.commit()
    conn.close()

##########################
    
def swissPairingsForTournament(tournID):

    # Returns a sorted list of player standings.
    playerStandingsList = playerStandingsForTournament(tournID)
    byePlayer = None
    
    swissPairingsList = []
    
    totalPlayers = len(playerStandingsList)
    #print("Total players: " + str(totalPlayers))
    
    i = 0
    while i < totalPlayers:
        if i+1 < totalPlayers:
            
            p1 = playerStandingsList[i]
            p2 = playerStandingsList[i+1]
            
            # Append the player's ID and name to the swiss pairings list.
            swissPairingsList.append((p1[0], p1[1], p2[0], p2[1]))
            #print("Pairing {0} (wins {1} opp {4}) with {2} (wins {3} opp {5})".format(p1[1], p1[6], p2[1], p2[6], p1[10], p2[10]))
            
        else:
            # Give a BYE to playerStandingsList[i]
            
            # Set return value
            byePlayer = p1
            pass
            
        i += 2
        
    return swissPairingsList, byePlayer
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Legacy function for older tournament tests.
  
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
    
    # Returns a sorted list of player standings.
    playerStandingsList = playerStandings()
    
    # Open DB.
    conn = connect()
    c = conn.cursor()
    
    # Get each player's details.
    c.execute("SELECT playerID, playerName from player;")
    allPlayers = c.fetchall()
    totalPlayers = len(allPlayers)

    swissPairingsList = []

    i = 0
    while i < totalPlayers:
        
        p1 = playerStandingsList[i]
        p2 = playerStandingsList[i+1]
        
        swissPairingsList.append((p1[0], p1[1], p2[0], p2[1]))
        
        i += 2
    
    # Get all existing players (Sort by number of wins).
    
    # Pair the first two up, then the next two, etc.
    
    # return the new list (id1, name1, id2, name2)
    return swissPairingsList

def playerStandingsForTournament(tournID):
    """Returns a list of the players and their win records, sorted by wins.
    Included as legacy support for old tournament tests.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
      tournID: the tournament the plyer standings should be taken for.

    Returns:
      A list of tuples, each of which contains:
        playerID: the player's unique id (assigned by the database)
        playerName: the player's full name (as registered)
        age: the age of the player
        gender: the gender of the player
        nationality: the nationality of the player
        
        tournamentID: the tournament as specified
        wins: the number of matches the player has won
        draws: the number of matches the player has drawn
        losses: the number of matches the player has lost
        totalGames: the number of matches the player has played
        opponentMatchWins: the number of matches the player's opponents have won
    """

     # Open DB.
    conn = connect()
    c = conn.cursor()
    query = ("SELECT playerID, playerName, age, gender, nationality,"
    " byeRounds, tournamentID, wins, draws, losses, totalGames, opponentMatchWins"
    " FROM playerAllTournsInfo WHERE tournamentID = %s"
    " ORDER BY wins DESC, opponentMatchWins DESC;")
    data = (tournID, )

    c.execute(query, data)
    allPlayers = c.fetchall()

    # Get each player's details.

    return allPlayers

def printSwissPairings(tournID, swissPairings, byePlayer):
    
    print("")
    print("------------------------")
    print("Recommended pairings for tournament {0}:".format(tournID))
    
    for pair in swissPairings:
        #0 - pID1
        #1 - pName1
        #2 - pID2
        #3 - pName2
        print("{0} ({1}) VS {2} ({3})".format(pair[1], pair[0], pair[3], pair[2]))
        
    if byePlayer is not None:
        
        print("Bye player: {0} ({1})".format(byePlayer[1], byePlayer[0]))

    print("------------------------")
    print("")

#######
## Legacy functions (to enable original tournament tests for older schema version)
#######

# Legacy function
def registerPlayer(playerName):
    """Adds a player to the tournament database. Included as legacy support for
    older tournament tests.

    Args:
      name: the player's full name (need not be unique).
    """

    tournName = "Tournament for legacy tests"

    # Connect to database
    conn = connect()
    c = conn.cursor()

    # Insert a new player with this name
    SQL = "INSERT INTO player (playerName) values (%s);"
    data = (playerName, )
    c.execute(SQL, data)

    # If the legacy tournament doesn't exist, 
    if getTournamentIDFromName(tournName) == None:
        SQL = "INSERT INTO tournament (tournamentName) values (%s);"
        data = (tournName, )
        c.execute(SQL, data)

    # Commit current changes.
    conn.commit()

    # Retrieve the newly created player, and legacy tournament.
    playerID = getPlayerIDFromName(playerName)
    tournID = getTournamentIDFromName(tournName)

    # Insert the player into the tournament.
    SQL = ("INSERT INTO tournamentPlayer (tournamentID, playerID)"
           " values (%s, %s);")
    data = (tournID, playerID)
    c.execute(SQL, data)

    # Close database connection
    conn.commit()
    conn.close()


# Legacy function
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    Included as legacy support for old tournament tests.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    tournID = getTournamentIDFromName("Tournament for legacy tests")

    # Simply calls the new playerStandings function, passing in the
    # legacy tournament as the specified tournament.
    newResult = playerStandingsForTournament(tournID)
    legacyResult = [(result[0], result[1], result[7], result[10]) for result in newResult]

    return legacyResult

# Legacy function
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players. Included as
    legacy support for old tournament tests.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    tournID = getTournamentIDFromName("Tournament for legacy tests")

    playMatch(tournID, winner, loser, "p1 wins")
    
