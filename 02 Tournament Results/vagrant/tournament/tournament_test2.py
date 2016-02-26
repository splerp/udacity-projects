#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *

def createSomePlayers():
    
    # Clear all players.
    # Clear all tournaments.
    
    addNewPlayer("Paul", 17, "M", "AUS")
    addNewPlayer("Carl", 19, "M", "AUS")
    addNewPlayer("Asdf", 3015, "M", "AUS")
    addNewPlayer("Mark", 24, "M", "AUS")
    addNewPlayer("Jenny", 23, "F", "AUS")
    addNewPlayer("Git", 22, "M", "AUS")
    addNewPlayer("Pebbles", 6, "M", "AUS")
    addNewPlayer("Goat", 12, "M", "AUS")
    
    addNewTournament("Dota 2 Historical 1st edition")
    

def testPlayers():

    clearAllData()

    tName = "Dota 2 Historical 1st edition"
    
    tID = getTournamentIDFromName(tName)

    p1ID = getPlayerIDFromName("Paul")
    p2ID = getPlayerIDFromName("Mark")
    p3ID = getPlayerIDFromName("Jenny")
    p4ID = getPlayerIDFromName("Pebbles")
    p5ID = getPlayerIDFromName("Goat")
    p6ID = getPlayerIDFromName("Carl")
    
    registerPlayer(tID, p1ID)
    registerPlayer(tID, p2ID)
    registerPlayer(tID, p3ID)
    registerPlayer(tID, p4ID)
    registerPlayer(tID, p5ID)
    registerPlayer(tID, p6ID)
    
    playMatch(tID, p1ID, p2ID, "p1 wins")
    playMatch(tID, p1ID, p2ID, "p1 wins")
    playMatch(tID, p3ID, p2ID, "draw")
    playMatch(tID, p3ID, p1ID, "draw")
    playMatch(tID, p3ID, p5ID, "p1 wins")
    
    tmp = playerRankingsView(tID)
    
    tmp = sorted(tmp, key=lambda player: player[3], reverse=True) # sort by total points
    
    print("----\nTournament: " + tName)
    for playerInfo in tmp:
        
        name = playerInfo[1]
        numGames = playerInfo[2]
        totalPoints = playerInfo[3]
        
        numGames = 0 if numGames == None else numGames
        totalPoints = 0 if totalPoints == None else totalPoints

        print("" + name + ": " + str(totalPoints) + " points (" + str(numGames) + " games)")
    
    print("----\n")
    
    print(tmp)
    


if __name__ == '__main__':
    #createSomePlayers()
    testPlayers()
    print "Success!  All tests pass!"
