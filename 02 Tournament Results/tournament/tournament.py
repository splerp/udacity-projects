#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
import argparse
import psycopg2


def connect():
    """
    Connect to the PostgreSQL database.  Returns a database
    connection and a cursor.
    """
    connection = psycopg2.connect("dbname=tournaments")
    cursor = connection.cursor()
    return connection, cursor


def clearAllData():
    """ Removes all existing data (excluding the swiss result values)"""
    conn, c = connect()

    c.execute("TRUNCATE player CASCADE")
    c.execute("TRUNCATE tournament CASCADE")
    c.execute("TRUNCATE tournamentMatch CASCADE")
    c.execute("TRUNCATE tournamentPlayer CASCADE")

    conn.commit()
    conn.close()


def addNewPlayer(name, age, gender, nationality):
    """Creates a new player for use in the system."""

    conn, c = connect()

    SQL = ("INSERT INTO player (playerName, age, gender, nationality)"
           "values (%s, %s, %s, %s)")
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
    """Given a player's name, delete that player."""

    conn, c = connect()

    SQL = "DELETE FROM player WHERE playerName=%s;"
    data = (name, )
    c.execute(SQL, data)

    conn.commit()
    conn.close()


def addByeRound(tournID, playerID):
    """Add a bye round to player in a particular tournament."""

    conn, c = connect()

    SQL = ("UPDATE tournamentPlayer SET byeRounds=byeRounds+1"
           " WHERE tournamentID=%s AND playerID=%s;")
    data = (tournID, playerID)
    c.execute(SQL, data)

    conn.commit()
    conn.close()


def getPlayerTournID(tournID, playerID):
    """
    Given a player ID and tournament ID, return
    the many-to-many (PlayerTournament) that they are associated with.
    """

    conn, c = connect()

    SQL = ("SELECT tournamentPlayerID FROM tournamentPlayer"
           " WHERE tournamentID = %s AND playerID = %s")
    data = (tournID, playerID)
    c.execute(SQL, data)

    theID = c.fetchone()

    conn.commit()
    conn.close()

    return theID


def registerPlayerByID(playerID, tournID):
    """Create a new PlayerTournament from a player ID and tournament ID."""

    conn, c = connect()

    SQL = ("INSERT INTO tournamentPlayer (tournamentID, playerID)"
           "values (%s,%s)")
    data = (tournID, playerID)
    c.execute(SQL, data)

    conn.commit()
    conn.close()


def getTournamentIDFromName(name):
    """Return the tournament ID that matches the given name."""

    conn, c = connect()

    SQL = "SELECT tournamentID FROM tournament WHERE tournamentName=%s"
    data = (name, )
    c.execute(SQL, data)

    toReturn = c.fetchone()

    conn.commit()
    conn.close()

    return None if toReturn is None else toReturn[0]


def countPlayersInTournament(tournID):
    """Returns the number of tournaments currently registered."""

    conn, c = connect()

    SQL = "SELECT count(*) FROM tournamentPlayer WHERE tournamentID = %s"
    data = (tournID,)
    c.execute(SQL, data)

    return c.fetchone()[0]


def getOpponentMatchWins(tournID, playerID):
    """Totals the wins of all the players this player has faced."""

    conn, c = connect()

    SQL = ("SELECT opponentTotalWins FROM opponentMatchWins"
           " WHERE tournamentID = %s AND playerID = %s")
    data = (tournID, playerID)
    c.execute(SQL, data)

    result = c.fetchone()

    return 0 if result is None else result[0]


def viewAllPlayers():
    """Retrive each player's basic information"""

    conn, c = connect()

    SQL = "SELECT playerID, playerName, age, gender, nationality FROM player;"
    c.execute(SQL)

    conn.close()


def addNewTournament(name):
    """
    Create a new tournament with the given name, and return
    the newly created tournament ID.
    """

    conn, c = connect()

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


def countTournaments():
    """Returns the number of tournaments currently in the system."""

    conn, c = connect()
    c.execute("SELECT count(*) FROM tournament")

    return c.fetchone()[0]


def playMatch(tournID, p1ID, p2ID, matchResult):
    """
    'Plays' a match - given a tournament and two players, and
    the result of this match, create a new tournamentMatch to
    store all this information.
    """

    # retrieve the torunament player ID from a player ID.
    pt1ID = getPlayerTournID(tournID, p1ID)
    pt2ID = getPlayerTournID(tournID, p2ID)

    conn, c = connect()

    SQL = ("INSERT INTO tournamentMatch (tournamentID, tournamentPlayer1ID,"
           " tournamentPlayer2ID, matchResult) VALUES (%s, %s, %s, %s)")
    data = (tournID, pt1ID, pt2ID, matchResult)
    c.execute(SQL, data)

    conn.commit()
    conn.close()


def playerStandingsForTournament(tournID):
    """
    Returns a list of the players and their win records, sorted by wins.
    Included as legacy support for old tournament tests.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

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
        opponentMatchWins: the number of matches the
        player's opponents have won
    """

    # Open DB.
    conn, c = connect()
    query = ("SELECT playerID, playerName, age, gender,"
             " nationality, byeRounds, tournamentID, wins,"
             " draws, losses, totalGames, opponentMatchWins"
             " FROM playerAllTournsInfo WHERE tournamentID = %s"
             " ORDER BY wins DESC, opponentMatchWins DESC;")
    data = (tournID, )

    c.execute(query, data)
    allPlayers = c.fetchall()

    # Get each player's details.

    return allPlayers


def swissPairingsForTournament(tournID):
    """
    Returns a sorted list of player standings (taking bye rounds into account).
    """

    playerStandingsList = playerStandingsForTournamentByeRoundOrdering(tournID)

    byePlayer = None
    swissPairingsList = []

    totalPlayers = len(playerStandingsList)

    i = 0
    while i < totalPlayers:
        if i+1 < totalPlayers:

            p1 = playerStandingsList[i]
            p2 = playerStandingsList[i+1]

            # Append the player's ID and name to the swiss pairings list.
            swissPairingsList.append((p1[0], p1[1], p2[0], p2[1]))

        else:
            # Give a BYE to playerStandingsList[i]
            p1 = playerStandingsList[i]

            # Set the return BYE player
            byePlayer = p1
            addByeRound(tournID, p1[0])

        i += 2

    return swissPairingsList, byePlayer


def playerStandingsForTournamentByeRoundOrdering(tournID):
    """
    Alternative ordering. Order by bye rounds (people with least
    number of bye rounds will always be at the bottom). Then, order
    by wins and opponentMatchWins - in reverse order. For example,
    3 players with a BYE and 3 without. If wins and OMW are not reverse
    ordered, the lowest-scoring player with 1 bye will be matched with
    the top-scoring player with 0 byes. Reverse order avoids this.
    """

    # Open DB and retrieve information from the playerAllTournsInfo view.
    conn, c = connect()
    query = ("SELECT playerID, playerName, age, gender,"
             " nationality, byeRounds, tournamentID, wins,"
             " draws, losses, totalGames, opponentMatchWins"
             " FROM playerAllTournsInfo WHERE tournamentID = %s"
             " ORDER BY byeRounds DESC, wins, opponentMatchWins;")
    data = (tournID, )

    c.execute(query, data)
    allPlayers = c.fetchall()

    # Get each player's details.
    return allPlayers


def printSwissPairings(tournID, swissPairings, byePlayer):
    """
    Displays an easy-to-read view of the given swiss pairings. For debugging.
    """

    print("")
    print("------------------------")
    print("Recommended pairings for tournament {0}:".format(tournID))

    for pair in swissPairings:
        # 0 - pID1
        # 1 - pName1
        # 2 - pID2
        # 3 - pName2
        print("{0} ({1}) VS {2} ({3})".format(pair[1], pair[0],
                                              pair[3], pair[2]))

    if byePlayer is not None:
        print("Bye player: {0} ({1})".format(byePlayer[1], byePlayer[0]))

    print("------------------------")
    print("")
