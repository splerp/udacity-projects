from __future__ import division
import random

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from data import SnakesAndLaddersGame, UserGame, SiteUser, HistoryStep

from google.appengine.ext import db

package = 'Hello'

# If the request contains path or querystring arguments,
# you cannot use a simple Message class.
# Instead, you must use a ResourceContainer class
REQUEST_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    name=messages.StringField(1),
    period=messages.StringField(2),
)

REQUEST_EMPTY = endpoints.ResourceContainer(
    message_types.VoidMessage
)

REQUEST_SITE_USER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    username=messages.StringField(1),
    password=messages.StringField(2),
    email=messages.StringField(3),
    description=messages.StringField(4)
)

REQUEST_CREATE_GAME_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    game_name=messages.StringField(1, default="A New Game"),
    player_name_1=messages.StringField(2, required=True),
    player_name_2=messages.StringField(3, required=True), # Make required
)

REQUEST_PLAY_TURN = endpoints.ResourceContainer(
    message_types.VoidMessage,
    game_name=messages.StringField(1),
    player_name=messages.StringField(2)
)

REQUEST_USER_GAMES = endpoints.ResourceContainer(
    message_types.VoidMessage,
    player_name=messages.StringField(1)
)

REQUEST_CANCEL_GAME = endpoints.ResourceContainer(
    message_types.VoidMessage,
    game_name=messages.StringField(1)
)

REQUEST_GAME_HISTORY = endpoints.ResourceContainer(
    message_types.VoidMessage,
    game_name=messages.StringField(1)
)

class BasicResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

class CreateGameResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    board = messages.StringField(3)

class CreateSiteUserResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    site_user_id = messages.StringField(3)

class PlayTurnResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    roll = messages.IntegerField(3)
    new_position = messages.IntegerField(4)

class PlayerGamesResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    games_in_progress = messages.StringField(3)
    games_completed = messages.StringField(4)

class PlayerRankingsResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    rankings = messages.StringField(3)

class GameHistoryResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    steps = messages.StringField(3)

@endpoints.api(name='snakesandladdersendpoints', version='v1')
class SnakesAndLaddersAPI(remote.Service):

    @endpoints.method(
        REQUEST_SITE_USER, CreateSiteUserResponse, http_method='POST',
        path = "createSiteUser", name = "createSiteUser")
    def create_site_user(self, request):

        user = SiteUser(
            username = request.username.lower(),
            password = request.password,
            email = request.email,
            description = request.description
        )
        user.save()

        return CreateSiteUserResponse(
            success=True,
            events=str([]),
            site_user_id=str(user.key()))

    @endpoints.method(
        REQUEST_EMPTY, PlayerRankingsResponse, http_method='GET',
        path = "playerRankings", name = "playerRankings")
    def player_rankings(self, request):

        rankings = []

        players = SiteUser.all()
        for player in players:

            wins = 0
            losses = 0
            for x in player.games:
                if x.game.game_state == 'complete':
                    if x.is_winner:
                        wins += 1
                    else:
                        losses += 1

            win_average = wins / (wins + losses) if (wins + losses) != 0 else 0

            rankings.append((player.username, wins, win_average))

        rankings.sort(key=lambda tuple: (tuple[1], tuple[2]), reverse=True)

        return PlayerRankingsResponse(
            success=True,
            events=str([]),
            rankings=str(rankings)
        )

    @endpoints.method(
        REQUEST_CANCEL_GAME, BasicResponse, http_method='POST',
        path = "cancelGame", name = "cancelGame")
    def cancelGame(self, request):

        success = False
        events = []

        game_to_cancel = db.GqlQuery("SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1", request.game_name.lower()).get()
        if game_to_cancel is None:
            events.append("Game '" + request.game_name.lower() + "' does not exist.")
        elif game_to_cancel.game_state == "cancelled" or game_to_cancel.game_state == "complete":
            events.append("Game cannot be cancelled because it is in state '" + game_to_cancel.game_state + "'.")
        else:
            game_to_cancel.game_state = "cancelled"
            game_to_cancel.save()

            success = True

        return BasicResponse(
            success=success,
            events=str(events)
        )

    @endpoints.method(
        REQUEST_USER_GAMES, PlayerGamesResponse, http_method='GET',
        path = "getUserGames", name = "getUserGames")
    def get_user_games(self, request):

        success = False
        events = []
        games_in_progress = []
        games_completed = []

        # Get user from name.
        user = db.GqlQuery("SELECT * FROM SiteUser WHERE username = :1", request.player_name.lower()).get()
        if user is None:
            events.append("No user exists with the name " + request.player_name.lower() + ".")
        else:
            for usergame in user.games:
                if usergame.game.game_state == "turn_p1":
                    games_in_progress.append(usergame.game.game_name)
                elif usergame.game.game_state == "turn_p2":
                    games_in_progress.append(usergame.game.game_name)
                elif usergame.game.game_state == "complete":
                    games_completed.append(usergame.game.game_name)

            success = True

        return PlayerGamesResponse(
            success=success,
            events=str(events),
            games_in_progress=str(games_in_progress),
            games_completed=str(games_completed)
        )

    @endpoints.method(
        REQUEST_GAME_HISTORY, GameHistoryResponse, http_method='GET',
        path = "getGameHistory", name = "getGameHistory")
    def get_game_history(self, request):

        success = False
        events = []

        steps = []

        # Get user from name.
        game = db.GqlQuery("SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1", request.game_name.lower()).get()
        if game is None:
            events.append("No game exists with name '" + request.game_name.lower() + "'.")
        else:

            for move in game.moves.order("move_num"):
                steps.append((
                    move.player_name,
                    move.roll_value,
                    move.hit_snake,
                    move.hit_ladder,
                    move.new_pos))

            success = True

        return GameHistoryResponse(
            success=success,
            events=str(events),
            steps=str(steps)
        )

    @endpoints.method(
        REQUEST_CREATE_GAME_CONTAINER, CreateGameResponse, http_method='POST',
        path = "createGame", name = "createGame")
    def create_game(self, request):

        success = False
        events = []

        player1 = db.GqlQuery("SELECT * FROM SiteUser WHERE username = :1", request.player_name_1.lower()).get()
        player2 = db.GqlQuery("SELECT * FROM SiteUser WHERE username = :1", request.player_name_2.lower()).get()

        existing_game = db.GqlQuery(
            "SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1",
            request.game_name.lower()).get()

        board_to_use = ""

        if existing_game is not None:
            events.append("EXISTING GAME WITH NAME " + request.game_name.lower())
        else:

            if player1 is None or player2 is None:
                events.append(
                    ("COULD NOT FIND BOTH PLAYERS for " + request.player_name_1.lower() +
                     "and " + request.player_name_2.lower()))

            else:

                board_to_use = convert_board_to_string(default_sal_board)

                # Create game with players.
                game = SnakesAndLaddersGame(
                    game_name = request.game_name.lower(),
                    game_board = board_to_use,
                )
                game.save()

                playerGame1 = UserGame(user=player1, game=game)
                playerGame1.save()

                playerGame2 = UserGame(user=player2, game=game)
                playerGame2.save()

                success = True
                events.append("You are starting a new game called {} with players {} and {}".format(
                    request.game_name, request.player_name_1, request.player_name_2))

        return CreateGameResponse(
            success=success,
            events=str(events),
            board=board_to_use)

    @endpoints.method(
        REQUEST_PLAY_TURN, PlayTurnResponse, http_method='POST',
        path = "playTurn", name = "playTurn")
    def play_turn(self, request):

        success = False
        events = []
        dice_roll=-1
        new_position = -1

        game = db.GqlQuery(
            "SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1",
            request.game_name.lower()).get()

        if game is None:
            events.append("Game does not exist! (" + request.game_name.lower() + ")")
        else:

            EXPECTED_PLAYERS = 2

            players = game.players.fetch(EXPECTED_PLAYERS)

            if len(players) != EXPECTED_PLAYERS:
                events.append(
                    ("Unexpected player count " + str(len(players)) +
                     " for game '" + game.game_name.lower() + "'. Expected: " + str(EXPECTED_PLAYERS)))
            else:

                player_1 = players[0]
                player_2 = players[1] # TODO When adding a game, player1 and player2 are specified. Use this for ordering

                # TODO Temporary; 'created' state will only be used if variable player count is implemented.
                if game.game_state == "created":
                    game.game_state = "turn_p1"

                if game.game_state != "turn_p1" and game.game_state != "turn_p2":
                    if game.game_state == "created":
                        events.append(
                            ("Waiting for players to join before starting the game."))
                    elif game.game_state == "complete":
                        events.append(
                            ("This game is already over."))
                    else:
                        events.append(
                            ("A turn cannot be done in state '" + game.game_state + "'."))

                elif request.player_name != player_1.user.username and request.player_name != player_2.user.username:
                    events.append(
                        ("Player '" + request.player_name + "' is not part of this game."))

                elif (game.game_state == "turn_p1" and request.player_name != player_1.user.username) or (game.game_state == "turn_p2" and request.player_name != player_2.user.username):
                    events.append(
                        ("It is not your turn, " + request.player_name + "."))

                else:

                    # Get player to update.
                    player = player_1 if game.game_state == "turn_p1" else player_2

                    # Play the turn...
                    dice_roll = random.randint(1, 6)
                    new_position = player.position + dice_roll

                    # Get board info to check for snakes and ladders.
                    current_board = convert_string_to_board(game.game_board)

                    # Check for ladders
                    hit_ladder = False
                    for ladder in current_board.ladders:
                        if ladder[0] == new_position:
                            hit_ladder = True
                            new_position = ladder[1]
                            game.ladders_hit += 1
                            events.append(
                                ("Hit a ladder!"))

                    # Check for snakes
                    hit_snake = False
                    for snake in current_board.snakes:
                        if snake[0] == new_position:
                            hit_snake = True
                            new_position = snake[1]
                            game.snakes_hit += 1
                            events.append(
                                ("Hit a snake..."))

                    # Update player location
                    player.position = new_position
                    game.total_moves += 1

                    # Check for win condition
                    if new_position >= current_board.size:
                        new_position = 100
                        game.game_state = "complete"
                        player.is_winner = True
                        events.append(
                            (player.user.username + " has won the game!"))
                    else:
                        if game.game_state == "turn_p1":
                            game.game_state = "turn_p2"
                        elif game.game_state == "turn_p2":
                            game.game_state = "turn_p1"

                    # Create a history step for game.
                    step = HistoryStep(
                        game=game,
                        move_num=game.total_moves,
                        player_name=player.user.username,
                        roll_value=dice_roll,
                        new_pos=new_position,
                        hit_snake=hit_snake,
                        hit_ladder=hit_ladder
                    )

                    success = True

                    player.save()
                    game.save()
                    step.save()

        return PlayTurnResponse(
            success=success,
            events=str(events),
            roll=dice_roll,
            new_position=new_position)

APPLICATION = endpoints.api_server([SnakesAndLaddersAPI])

class SALBoard():
    size = 100
    snakes = []
    ladders = []
    def __init__(self, size, snakes, ladders):
        self.size = size
        self.snakes = snakes
        self.ladders = ladders

default_sal_board = SALBoard(
    size = 100,
    snakes=[(15, 2), (23, 9), (65, 50), (91, 14)],
    ladders=[(5, 20), (6, 50), (61, 87), (43, 97)]
)

def convert_board_to_string(board):
    # FIXME Do not store an empty element; do not add a . to the end of the string.
    # Add size.
    to_return = "" + str(board.size) + ":"
    # Add snakes.
    for snake in board.snakes:
        to_return += str(snake[0]) + "," + str(snake[1]) + "."
    to_return += ":"
    # Add ladders.
    for ladder in board.ladders:
        to_return += str(ladder[0]) + "," + str(ladder[1]) + "."
    return to_return

def convert_string_to_board(the_string):

    (size_str, snakes_str, ladders_str) = the_string.split(':')
    size = int(size_str)

    snakes = []
    snakes_str = snakes_str.split('.')
    for snake_str in snakes_str:
        if snake_str != '':
            (x, y) = snake_str.split(',')
            snakes.append((int(x), int(y)))

    ladders = []
    ladders_str = ladders_str.split('.')
    for ladder_str in ladders_str:
        if ladder_str != '':
            (x, y) = ladder_str.split(',')
            ladders.append((int(x), int(y)))

    return SALBoard(
        size = size,
        snakes=snakes,
        ladders=ladders
    )

def remove_all_data():

    for x in SnakesAndLaddersGame.all():
        x.delete()

    for x in SiteUser.all():
        x.delete()

    for x in UserGame.all():
        x.delete()