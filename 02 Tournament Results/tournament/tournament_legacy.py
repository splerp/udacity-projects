#!/usr/bin/env python
# tournament_legacy.py -- an extension of tournament.py that provides backwards
# compatibility for an older database schema.
import argparse
import psycopg2
import tournament as main


def registerPlayer(playerName):
    """
    Adds a player to the tournament database. Included as legacy support for
    older tournament tests.

    Args:
      name: the player's full name (need not be unique).
    """

    tournName = "Tournament for legacy tests"

    # Connect to database
    conn, c = main.connect()

    # Insert a new player with this name
    SQL = "INSERT INTO player (playerName) values (%s);"
    data = (playerName, )
    c.execute(SQL, data)

    # If the legacy tournament doesn't exist,
    if main.getTournamentIDFromName(tournName) == None:
        SQL = "INSERT INTO tournament (tournamentName) values (%s);"
        data = (tournName, )
        c.execute(SQL, data)

    # Commit current changes.
    conn.commit()

    # Retrieve the newly created player, and legacy tournament.
    playerID = getPlayerIDFromName(playerName)
    tournID = main.getTournamentIDFromName(tournName)

    # Insert the player into the tournament.
    SQL = ("INSERT INTO tournamentPlayer (tournamentID, playerID)"
           " values (%s, %s);")
    data = (tournID, playerID)
    c.execute(SQL, data)

    # Close database connection
    conn.commit()
    conn.close()


def getPlayerIDFromName(name):
    """Return the player ID for the name specified."""

    # Connect to the database.
    conn, c = main.connect()

    # Select the player that matches the name.
    SQL = "SELECT playerID FROM player WHERE playerName=%s"
    data = (name, )
    c.execute(SQL, data)

    toReturn = c.fetchone()

    conn.commit()
    conn.close()

    # Only return the first result
    return toReturn[0]


# Legacy function
def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.
    Included as legacy support for old tournament tests.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    tournID = main.getTournamentIDFromName("Tournament for legacy tests")

    # Simply calls the new playerStandings function, passing in the
    # legacy tournament as the specified tournament.
    newResult = main.playerStandingsForTournament(tournID)
    legacyResult = [(result[0], result[1],
                     result[7], result[10]) for result in newResult]

    return legacyResult


# Legacy function
def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players. Included as
    legacy support for old tournament tests.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    tournID = main.getTournamentIDFromName("Tournament for legacy tests")

    main.playMatch(tournID, winner, loser, "p1 wins")


def deleteMatches():
    """Remove all the match records from the database."""

    conn, c = main.connect()

    c.execute("TRUNCATE tournamentMatch")

    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn, c = main.connect()
    c.execute("SELECT count(*) FROM player")

    return c.fetchone()[0]


def deletePlayers():
    """Remove all the player records from the database."""

    conn, c = main.connect()

    c.execute("TRUNCATE player CASCADE")

    conn.commit()
    conn.close()


def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.
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
    conn, c = main.connect()

    # Get each player's details.
    c.execute("SELECT playerID, playerName from player;")
    allPlayers = c.fetchall()
    totalPlayers = len(allPlayers)

    swissPairingsList = []

    # As this is a legacy function, bye rounds should not be accounted for.
    i = 0
    while i < totalPlayers:

        p1 = playerStandingsList[i]
        p2 = playerStandingsList[i+1]

        swissPairingsList.append((p1[0], p1[1], p2[0], p2[1]))

        i += 2

    # return the new list (id1, name1, id2, name2)
    return swissPairingsList
