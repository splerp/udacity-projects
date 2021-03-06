# Project 2 - Tournament Results
A collection of scripts to generate and test a database that stores players, tournaments, and each game players have participated in.

## Installation
#### Prerequisites
To use the bash environment, Git should be installed. [[link](https://git-scm.com/)]

VirtualBox must be installed to create the virtual machine. [[link](https://www.virtualbox.org/)]

Vagrant must be installed to run the vagrant virtual machine. [[link](https://www.vagrantup.com/)]

#### Starting the vagrant machine (Windows)
1. Navigate to the directory which contains "VagrantFile" (base directory)
2. Start a new Git Bash at this location
3. Type "vagrant up" (start the vagrant virtual machine)
4. Type "vagrant ssh" (connect to the machine)

## Usage
#### Creating the database
1. In the virtual machine in Git Bash, run the `psql` command
2. Type `\i tournament.sql` to run the migrations and fixtures to create the database with all required tables, fixtures, and views.

#### Running the scripts
1. In the virtual machine, navigate to /vagrant/tournament (`cd /vagrant/tournament`)
2. To use the tests for the initial database schema, run `python tournament_test.py`
3. To use the tests for the extended database schema, run `python tournamnet_test2.py`

## Initial database schema
- Players can be registered for a single tournament
- The number of wins for each player can be calculated
- The swiss pairings for the tournament (based on player wins) can be calculated

## Extended database schema
- Multiple tournaments are supported, so any player can register for any number of them
- If there is an uneven number of players, a bye round is given to one player. Steps are taken to ensure players each receive a minimal number of bye rounds
- As well as winning and losing, players can draw in a match
- When two players have an equal number of wins, they will be ordered depending on the number of opponent match wins (OMW). This is the sum of wins for each of this particular player's opponents

## Database Structure
The tournament database structure aims to be as simple as possible, while providing more complicated views when more detailed information is required.

#### Tournament table
Stores information about each tournament registered in the database.

#### Player table
Stores information about each player registered in the database.

#### TournamentPlayer table
When a player signs up for a particular tournament, a new TournamentPlayer entry is created. This table also keeps track of the number of bye rounds a player has had for this tournament.

#### TournamentMatch table
Each entry represents a different game that two players have played between each other.

#### SwissResult table
The swiss result table contains all the different possible outcomes of the match, and how much each player scores depending on that result.

## Database views
The database also defines views for more complicated data visualisation. The most important views are:

#### OpponentMatchWins view
Returns a table that, for each player in each tournament, displays how many matches all of their opponents combined have won.

#### PlayerAllTournsInfo view
Combines each player's information with their number of wins, draws, losses, and games played, as well as their opponent match wins. This view also relies on other views such as IndividualTournamentPlayerWins for its information.

## Code layout
- tournament.sql: Contains all table and view definitions for the database
- tournament.py: Contains all code for the updated database schema to query the database
- tournament_legacy.py: Contains all functions to support the original database tests
- tournament_test.py: All original tests for the old, more basic database schema
- tournament_test2.py: All tests for the new, updated database schema

## Code base

The content of `tournament.py`, `tournament_test.py` and `tournament.sql` was originally created by Udacity for the Full Stack Developer course. [[link](https://github.com/adarsh0806/udacity-full-stack/tree/master/p2)]
