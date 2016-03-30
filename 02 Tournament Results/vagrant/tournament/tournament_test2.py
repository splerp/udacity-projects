#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# These additional tests are for the added functionality for each of the
# implemented additional features.

from tournament import *

def testPlayerOpponentMatchWins():

    clearAllData()

    # Check that tournaments can be added.
    t1ID = addNewTournament("8 player swiss pairing test")

    # Check that players can be added to a tournament.
    p1ID = addNewPlayer("Mango", 25, "M", "AUS")
    p2ID = addNewPlayer("Potato", 28, "F", "EU")
    p3ID = addNewPlayer("Chair", 27, "M", "NA")
    p4ID = addNewPlayer("Dog", 9, "M", "AUS")
    p5ID = addNewPlayer("Lempika", 25, "M", "JP")
    p6ID = addNewPlayer("Meringue", 28, "F", "AUS")
    p7ID = addNewPlayer("Lamp", 27, "M", "AUS")
    p8ID = addNewPlayer("Paul", 20, "M", "AUS")
    
    registerPlayerByID(p1ID, t1ID)
    registerPlayerByID(p2ID, t1ID)
    registerPlayerByID(p3ID, t1ID)
    registerPlayerByID(p4ID, t1ID)
    registerPlayerByID(p5ID, t1ID)
    registerPlayerByID(p6ID, t1ID)
    registerPlayerByID(p7ID, t1ID)
    #registerPlayerByID(p8ID, t1ID)

    # Round 1
    #playMatch(t1ID, p1ID, p8ID, "p1 wins")
    playMatch(t1ID, p2ID, p7ID, "p1 wins")
    playMatch(t1ID, p3ID, p4ID, "p1 wins")
    playMatch(t1ID, p5ID, p6ID, "p1 wins")

    swissPairings1, byePlayer1 = swissPairingsForTournament(t1ID)
    #printSwissPairings(t1ID, swissPairings1, byePlayer1)
    
    # Round 2
    playMatch(t1ID, p7ID, p1ID, "p1 wins")
    playMatch(t1ID, p4ID, p2ID, "p1 wins")
    playMatch(t1ID, p3ID, p5ID, "p1 wins")
    #playMatch(t1ID, p6ID, p8ID, "p1 wins")
    
    swissPairings1, byePlayer1 = swissPairingsForTournament(t1ID)
    #printSwissPairings(t1ID, swissPairings1, byePlayer1)
    
    # Round 3
    playMatch(t1ID, p1ID, p5ID, "p1 wins")
    playMatch(t1ID, p2ID, p6ID, "p1 wins")
    playMatch(t1ID, p4ID, p3ID, "p1 wins")
    #playMatch(t1ID, p7ID, p8ID, "p1 wins")

    swissPairings1, byePlayer1 = swissPairingsForTournament(t1ID)
    printSwissPairings(t1ID, swissPairings1, byePlayer1)

    print("All player opponent match wins passed.")

def testPlayerStandings():
    
    clearAllData()
    
    t1ID = addNewTournament("4 player exciting stuff")
    
    p1ID = addNewPlayer("Mango", 25, "M", "AUS")
    p2ID = addNewPlayer("Potato", 28, "F", "EU")
    p3ID = addNewPlayer("Chair", 27, "M", "NA")
    p4ID = addNewPlayer("Dog", 9, "M", "AUS")
    
    registerPlayerByID(p1ID, t1ID)
    registerPlayerByID(p2ID, t1ID)
    registerPlayerByID(p3ID, t1ID)
    registerPlayerByID(p4ID, t1ID)
    
    # Should all be 0.
    compareEqual("Player {} opponent match wins".format(p1ID), getOpponentMatchWins(t1ID, p1ID), 0)
    compareEqual("Player {} opponent match wins".format(p2ID), getOpponentMatchWins(t1ID, p2ID), 0)
    compareEqual("Player {} opponent match wins".format(p3ID), getOpponentMatchWins(t1ID, p3ID), 0)
    compareEqual("Player {} opponent match wins".format(p4ID), getOpponentMatchWins(t1ID, p4ID), 0)
    
    playMatch(t1ID, p1ID, p2ID, "p1 wins")
    playMatch(t1ID, p1ID, p3ID, "p1 wins")
    playMatch(t1ID, p1ID, p4ID, "p1 wins")
    
    playMatch(t1ID, p2ID, p4ID, "p1 wins")
    
    playMatch(t1ID, p3ID, p2ID, "p1 wins")
    playMatch(t1ID, p3ID, p4ID, "p1 wins")
    
    compareEqual("Player {} opponent match wins".format(p1ID), getOpponentMatchWins(t1ID, p1ID), 3)
    compareEqual("Player {} opponent match wins".format(p2ID), getOpponentMatchWins(t1ID, p2ID), 5)
    compareEqual("Player {} opponent match wins".format(p3ID), getOpponentMatchWins(t1ID, p3ID), 4)
    compareEqual("Player {} opponent match wins".format(p4ID), getOpponentMatchWins(t1ID, p4ID), 6)

    print("All player standings tests passed.")
    

def testTournaments():

    clearAllData()

    compareEqual("Tournament count", countTournaments(), 0)

    # Check that tournaments can be added.
    t1ID = addNewTournament("Chess Championships 2016")
    t2ID = addNewTournament("CS:GO - IEM Katowice 2016")
    t3ID = addNewTournament("TF2 6s Beta Test #3")

    compareEqual("Tournament count", countTournaments(), 3)

    # Check that players can be added to a tournament.
    p1ID = addNewPlayer("Mango", 25, "M", "AUS")
    p2ID = addNewPlayer("Potato", 28, "F", "EU")
    p3ID = addNewPlayer("Chair", 27, "M", "NA")
    p4ID = addNewPlayer("Dog", 9, "M", "AUS")

    registerPlayerByID(p1ID, t1ID)
    registerPlayerByID(p2ID, t1ID)
    
    registerPlayerByID(p1ID, t2ID)
    registerPlayerByID(p2ID, t2ID)
    registerPlayerByID(p3ID, t2ID)
    registerPlayerByID(p4ID, t2ID)

    registerPlayerByID(p2ID, t3ID)
    registerPlayerByID(p3ID, t3ID)
    registerPlayerByID(p4ID, t3ID)

    compareEqual("Tourn 1 player count", countPlayersInTournament(t1ID), 2)
    compareEqual("Tourn 2 player count", countPlayersInTournament(t2ID), 4)

    # Check that players are matched up correctly
    playMatch(t2ID, p1ID, p2ID, "p1 wins")
    playMatch(t2ID, p3ID, p4ID, "p2 wins")
    playMatch(t2ID, p3ID, p2ID, "p2 wins")

    playMatch(t3ID, p2ID, p4ID, "p1 wins")
    playMatch(t3ID, p2ID, p4ID, "p1 wins")
    playMatch(t3ID, p2ID, p4ID, "p1 wins")
    playMatch(t3ID, p3ID, p4ID, "p1 wins")
    playMatch(t3ID, p2ID, p4ID, "draw")
    playMatch(t3ID, p2ID, p4ID, "draw")

    standingsTourn1 = playerStandingsForTournament(t1ID)
    standingsTourn2 = playerStandingsForTournament(t2ID)
    standingsTourn3 = playerStandingsForTournament(t3ID)

    # No matches were played in tourn 1, so check that everything is 0.
    for(playerID, playerName, playerAge, playerGender, playerNationality, playerByeRounds, tournID, wins, draws, losses, totalGames, opponentWins) in standingsTourn1:

        compareEqual("Player {} total games played".format(playerID), totalGames, 0)
        compareEqual("Player {} number of wins".format(playerID), wins, 0)
        compareEqual("Player {} number of losses".format(playerID), losses, 0)
        compareEqual("Player {} number of draws".format(playerID), draws, 0)

    # Check that wins, losses, and games played are set correctly.
    for(playerID, playerName, playerAge, playerGender, playerNationality, playerByeRounds,tournID, wins, draws, losses, totalGames, opponentWins) in standingsTourn2:
        
        if playerID == p1ID or playerID == p4ID:
            compareEqual("Player {} total games played".format(playerID), totalGames, 1)
            compareEqual("Player {} number of wins".format(playerID), wins, 1)
            compareEqual("Player {} number of losses".format(playerID), losses, 0)

        elif playerID == p2ID:
            compareEqual("Player {} total games played".format(playerID), totalGames, 2)
            compareEqual("Player {} number of wins".format(playerID), wins, 1)
            compareEqual("Player {} number of losses".format(playerID), losses, 1)

        elif playerID == p3ID:
            compareEqual("Player {} total games played".format(playerID), totalGames, 2)
            compareEqual("Player {} number of wins".format(playerID), wins, 0)
            compareEqual("Player {} number of losses".format(playerID), losses, 2)
    
    print("All tournament tests passed.")
        

def compareEqual(valueName, value, expectedValue):
    if(value != expectedValue):
        raise ValueError("{} should be equal to {} (actual: {}).".format(valueName, expectedValue, value))

def compareLessThan(valueName, value, expectedValue):
    if(value >= expectedValue):
        raise ValueError("{} should be less than {} (actual: {}).".format(valueName, expectedValue, value))


def testPlayers():

    clearAllData()

    tName = "Dota 2 Historical 1st edition"
    tName2 = "Unpopular tournament (still fun though)"
    tName3 = "TF2 Highlander Competition 2025 B.C."
    
    # Initial player / tournament data.
    addNewPlayer("Paul", 17, "M", "AUS")
    addNewPlayer("Carl", 19, "M", "AUS")
    addNewPlayer("Asdf", 3015, "M", "AUS")
    addNewPlayer("Mark", 24, "M", "AUS")
    addNewPlayer("Jenny", 23, "F", "AUS")
    addNewPlayer("Git", 22, "M", "AUS")
    addNewPlayer("Pebbles", 6, "M", "AUS")
    addNewPlayer("Goat", 12, "M", "AUS")
    
    addNewTournament(tName)
    tID = getTournamentIDFromName(tName)
    
    addNewTournament(tName2)
    t2ID = getTournamentIDFromName(tName2)
    
    addNewTournament(tName3)
    t3ID = getTournamentIDFromName(tName3)
    
    p1ID = getPlayerIDFromName("Paul")
    p2ID = getPlayerIDFromName("Carl")
    p3ID = getPlayerIDFromName("Asdf")
    p4ID = getPlayerIDFromName("Mark")
    p5ID = getPlayerIDFromName("Jenny")
    p6ID = getPlayerIDFromName("Git")
    
    registerPlayerByID(p1ID, tID)
    registerPlayerByID(p2ID, tID)
    registerPlayerByID(p3ID, tID)
    registerPlayerByID(p4ID, tID)
    registerPlayerByID(p5ID, tID)
    registerPlayerByID(p6ID, tID)
    
    registerPlayerByID(p1ID, t2ID)
    registerPlayerByID(p2ID, t2ID)
    registerPlayerByID(p4ID, t2ID)
    
    registerPlayerByID(p2ID, t3ID)
    registerPlayerByID(p4ID, t3ID)
    
    player1TournID = getPlayerTournID(tID, p1ID)
    player2TournID = getPlayerTournID(tID, p2ID)
    player3TournID = getPlayerTournID(tID, p3ID)
    player4TournID = getPlayerTournID(tID, p4ID)
    player5TournID = getPlayerTournID(tID, p5ID)
    
    playMatch(tID, p1ID, p2ID, "p1 wins")
    playMatch(tID, p1ID, p2ID, "p1 wins")
    playMatch(tID, p2ID, p1ID, "p2 wins")
    playMatch(tID, p3ID, p2ID, "draw")
    playMatch(tID, p3ID, p1ID, "draw")
    playMatch(tID, p3ID, p5ID, "p1 wins")
    playMatch(tID, p5ID, p4ID, "p2 wins")
    
    playMatch(t2ID, p2ID, p1ID, "p2 wins")
    
    playMatch(t3ID, p2ID, p4ID, "p1 wins")
    playMatch(t3ID, p2ID, p4ID, "p1 wins")
    playMatch(t3ID, p2ID, p4ID, "draw")
    playMatch(t3ID, p2ID, p4ID, "unfinished")
    
    print("All player tests passed.")
    


if __name__ == '__main__':
    #createSomePlayers()
    testPlayers()
    testTournaments()
    testPlayerStandings()
    testPlayerOpponentMatchWins()
    viewAllPlayers()
    print("--All tests passed--")
