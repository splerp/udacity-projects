# Project 4 - Design a Game
Google App Engine implementation of a Snakes and Ladders online application. Uses API endpoints to standardise server requests.

## Installation
No installation required - visit the website here:
#### [udacity-game-design.appspot.com](https://udacity-game-design.appspot.com)

## Usage
#### Registering
1. From the main page, click on "sign up".
2. Choose a name and password, and specify an optional email address. **This address will be used to send reminder emails to.**
3. Click the register button.

#### Logging In
1. From the main page, click on "Login here!".
2. Enter your username and password.
3. Click the Log In button.

#### Viewing a list of games
- The main page should display all games you are currently a part of.
- On the main navigation panel, click on "View my games" to display a list of all the games you are currently a part of.
- On the main navigation panel, click on "Join a game" to display all games that are still waiting for players to join.

#### Creating a new game
1. On the main navigation panel, click "Create!".
2. Choose a title for the new game and submit it.
3. You will automatically be redirected to the game's page.

#### Playing a game
1. At least 2 players must join the game. To join a game, navigate to the game's page and click the "Join game" button.
2. Once two players have joined, the owner can now click the "Start Game" button to begin playing.
3. When it is the current player's turn, they must click the "Play my turn" button.
4. The game will end when a player reaches the final square, winning the game.


## API Endpoint Descriptions
API endpoints can be accessed here: [[link](https://udacity-game-design.appspot.com/_ah/api/explorer)]
All endpoints are part of the SnakesAndLaddersEndpoints API.

** All API endpoints are standardised** to always return at least two properties: "events" and "success". "Success" is either true or false and simply notfies whether the request was successful for not. The "events" property is a string-encoded list of messages (e.g. error messages on fail, points of interests on success).

#### createSiteUser
**Fields:**
- username (required - must be unique)
- password (required)
- email
- description

**Additionally returns:** site_user_id - The new user's unique ID.

#### createGame
**Fields:**
- game_name (required - must be unique)

**Additionally returns:** game_key - the game's unique ID. board - the definition of the new game board in string form.

#### cancelGame
**Fields:**
- game_name (The unique identifier of the game to be cancelled)

**Additionally returns:** Nothing

#### joinGame
**Fields:**
- game_name (required)
- player_name (required)

**Additionally returns:** Nothing

The player specified will join the game specified (if the game is in "waiting for players" state).

#### startGame
**Fields:**
- game_name (required)

**Additionally returns:** next_player - the next player that should play their turn.

Transitions the game from "waiting for players" to "playing".

#### playTurn
**Fields:**
- game_name (required)
- player_name (required)

**Additionally returns:** next_player - the next player that should play their turn. new_position - where the player ended up. roll - what the player rolled.

If the game is valid and it is currently the given player's turn, their turn is played out.

#### getGameHistory
**Fields:**
- game_name (required)

**Additionally returns:** steps - a string-encoded list of moves made in this game. Includes player that moved, if they hit a ladder, if they hit a snake etc.

Returns all the player moves that are associated with the given game.

#### getUserGames
**Fields:**
- player_name (required)

**Additionally returns:** games_completed - string-encoded list of games that this player has completed. games_in_progress - string-encoded list of games that this player ahs started, but not yet completed.

Returns lists of games that the player has completed, and is currently part of.

#### playerRankings
**Fields:** None

**Additionally returns:** rankings - string-encoded list of players, their total wins, their total losses and their win / loss ratio all sorted in order of leaderboard position.

Returns all players with some statistics to determine their ranking.

## Database Structure
The various data stored in the Google App Engine database is structured using these entities:

#### SiteUser
Stores information about a registered user.

#### SnakesAndLaddersGame
Stores information about a snakes and ladders game. This includes the board data (positions of snakes and ladders etc.) and the current game state.

#### UserGame
Relationship data between users and games (i.e. stores a game reference and a player reference). Stores whether a user is the owner of a game, whether they're the winner of a game, and their current position on the game board.

#### HistoryStep
Stores information about all the moves taken during a particular game. This includes the player that moved, the number they rolled, where they ended up, and if they hit a snake or a ladder.

## Code layout
- main.py: Entry point for program. Defines handlers for main pages of site and all routing information, including cron jobs and tasks.

#### src/ folder
- game_api.py: Contains definition for the Snakes and Ladders API, including definitions for all API endpoints.
- data.py: Contains definitions for database models.
- route.py: Base Handler class is defined here.
- security.py: All functions that interact with cookies and validating users / passwords.
- validation.py: Functions that handler registration / login validation.

#### static/ folder
- All content for use on the site.
- scripts/ folder
	- Javascript files.
- style/ folder
	- CSS files.


#### templates/ folder
- Each file contains a separate jinja template. base.html defines the base page contents.

## Code base
The structure of this site is based on the content of the Full Stack Developer course by Udacity. [[link](https://github.com/adarsh0806/udacity-full-stack)]

Udacity's Design-A-Game repository was used as a reference for creating cron jobs and using the task queue. [[link](https://github.com/udacity/FSND-P4-Design-A-Game)]