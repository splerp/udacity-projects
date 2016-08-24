from __future__ import division

import endpoints
import json
import random

from protorpc import messages
from protorpc import message_types
from protorpc import remote
from data import (
    SnakesAndLaddersGame, UserGame, SiteUser, HistoryStep,
    convert_board_to_string, convert_string_to_board, default_sal_board)

from google.appengine.ext import db
from google.appengine.api import taskqueue

import src.security as security
from src.validation import validate_register
from src.dbextensions import get_rankings

"""Hello World API implemented using Google Cloud Endpoints.

Contains declarations of endpoint, endpoint methods,
as well as the ProtoRPC message class and container required
for endpoint method definition.
"""
package = 'SplGame'

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
    # player_name_1=messages.StringField(2, required=True),
    # player_name_2=messages.StringField(3, required=True), # Make required
)

"""class RequestCreateGameClass(messages.Message):
    game_name = messages.StringField(1)"""


REQUEST_JOIN_GAME = endpoints.ResourceContainer(
    message_types.VoidMessage,
    game_name=messages.StringField(1, required=True),
    player_name=messages.StringField(2, required=True)
)

REQUEST_PLAY_TURN = endpoints.ResourceContainer(
    message_types.VoidMessage,
    game_name=messages.StringField(1),
    player_name=messages.StringField(2)
)

REQUEST_START_GAME = endpoints.ResourceContainer(
    message_types.VoidMessage,
    game_name=messages.StringField(1)
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

    game_key = messages.StringField(3)
    board = messages.StringField(4)


class JoinGameResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)


class CreateSiteUserResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    site_user_id = messages.StringField(3)


class PlayTurnResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    roll = messages.IntegerField(3)
    new_position = messages.IntegerField(4)
    next_player = messages.StringField(5)


class StartGameResponse(messages.Message):
    success = messages.BooleanField(1)
    events = messages.StringField(2)

    next_player = messages.StringField(3)

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

        name = request.username.lower()
        pass1 = request.password
        pass2 = request.password
        email = request.email

        error_messages = validate_register(name, pass1, pass2, email)

        user_key = None
        if len(error_messages) == 0:
            user = SiteUser(
                username=name,
                password=security.make_pw_hash(
                    name,
                    pass1,
                    security.make_salt()),
                email=email)
            user.put()
            user_key = user.key()

        return CreateSiteUserResponse(
            success=True,
            events=str(error_messages),
            site_user_id=str(user_key))

    @endpoints.method(
        REQUEST_EMPTY, PlayerRankingsResponse, http_method='GET',
        path="playerRankings", name="playerRankings")
    def player_rankings(self, request):

        rankings = get_rankings()

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

        game_to_cancel = db.GqlQuery(
            "SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1",
            request.game_name.lower()).get()

        if game_to_cancel is None:
            events.append(
                "Game '" + request.game_name.lower() + "' does not exist.")
        elif (game_to_cancel.game_state == "cancelled"
            or game_to_cancel.game_state == "complete"):
            events.append(
                "Game cannot be cancelled because it is in state '" + game_to_cancel.game_state + "'.")
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
        path="getUserGames", name="getUserGames")
    def get_user_games(self, request):

        success = False
        events = []
        games_in_progress = []
        games_completed = []

        # Get user from name.
        user = db.GqlQuery(
            "SELECT * FROM SiteUser WHERE username = :1",
            request.player_name.lower()).get()

        if user is None:
            events.append(
                "No user exists with the name " + request.player_name.lower() + ".")
        else:
            for usergame in user.games:
                if usergame.game.game_state == "playing":
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
        path="getGameHistory", name="getGameHistory")
    def get_game_history(self, request):

        success = False
        events = []

        steps = []

        # Get user from name.
        game = db.GqlQuery(
            "SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1",
            request.game_name.lower()).get()

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
        path="createGame", name="createGame")
    def create_game(self, request):

        success = False
        events = []

        existing_game = db.GqlQuery(
            "SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1",
            request.game_name.lower()).get()

        board_to_use = ""

        if existing_game is not None:
            events.append(
                "EXISTING GAME WITH NAME " + request.game_name.lower())
        else:

            board_to_use = convert_board_to_string(default_sal_board)

            # Create game with players.
            game = SnakesAndLaddersGame(
                game_name=request.game_name.lower(),
                game_board=board_to_use,
            )
            game.save()

            success = True
            events.append(
                "You are starting a new empty game called {}".format(
                    request.game_name))

        return CreateGameResponse(
            success=success,
            events=str(events),
            game_key=str(game.key()),
            board=board_to_use)


    @endpoints.method(
        REQUEST_JOIN_GAME, JoinGameResponse, http_method='POST',
        path="joinGame", name="joinGame")
    def join_game(self, request):

        success = False
        events = []

        site_user = db.GqlQuery(
            "SELECT * FROM SiteUser WHERE username = :1",
            request.player_name.lower()).get()

        game = db.GqlQuery(
            "SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1",
            request.game_name.lower()).get()

        if game is None:
            events.append("No game found with the name " + request.game_name.lower())
        elif game.game_state != "created":
            events.append("Players can only join before a game has started. ")
        elif site_user is None:
            events.append("No player found with the name " + request.game_name.lower())
        elif site_user.username in [player.user.username for player in game.players]:
            events.append("Player " + request.game_name.lower() + " is already in this game.")
        else:

            newUserGame = UserGame(user=site_user, game=game, player_num=(game.num_players() + 1))
            newUserGame.save()

            game.current_player_num = 1 if game.current_player_num == 0 else game.current_player_num
            game.save()

            success = True
            events.append("{} has successfully joined {}!".format(
                site_user.username, request.game_name))

            taskqueue.add(
                url='/tasks/email_game_join',
                params={'user': site_user.key(),
                        'game_name': request.game_name}
            )

        return JoinGameResponse(
            success=success,
            events=str(events))



    @endpoints.method(
        REQUEST_PLAY_TURN, PlayTurnResponse, http_method='POST',
        path="playTurn", name="playTurn")
    def play_turn(self, request):

        success = False
        events = []
        dice_roll=-1
        new_position = -1
        next_player = None

        request_name = request.player_name.lower()

        game = db.GqlQuery(
            "SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1",
            request.game_name.lower()).get()

        if game is None:
            events.append("Game does not exist! (" + request.game_name.lower() + ")")
        else:

            total_players = game.num_players()

            players = game.players.fetch(total_players)

            if len(players) != total_players:
                events.append(
                    ("Unexpected player count " + str(len(players)) +
                     " for game '" + game.game_name.lower() + 
                     "'. Expected: " + str(total_players)))
            else:

                # Get player to update (if any).
                expected_player = game.players.filter(
                    "player_num =", game.current_player_num).get()

                if game.game_state != "playing":
                    if game.game_state == "created":
                        events.append(
                            ("Waiting for players to join before starting the game."))
                    elif game.game_state == "complete":
                        events.append(
                            ("This game is already over."))
                    else:
                        events.append(
                            ("A turn cannot be done in state '" +
                            game.game_state + "'."))
                else:

                    # At this point, set next_player (good for the user to know about)
                    next_player = game.players.filter(
                        "player_num =",
                        game.current_player_num).get().user.username

                    if request_name not in [player.user.username for player in players]:
                        events.append(
                            ("Player '" + request_name + "' is not part of this game."))

                    elif (request_name != expected_player.user.username):
                        events.append(
                            ("It is not your turn, " + request_name + "."))

                    else:

                        # Play the turn...
                        dice_roll = random.randint(1, 6)
                        new_position = expected_player.position + dice_roll

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
                        expected_player.position = new_position
                        game.total_moves += 1

                        # Check for win condition
                        if new_position >= current_board.size:
                            new_position = 100
                            game.game_state = "complete"
                            expected_player.is_winner = True
                            events.append(
                                (expected_player.user.username + " has won the game!"))
                        else:
                            game.game_state = "playing"

                            # Move onto next player
                            game.current_player_num = expected_player.player_num + 1
                            game.current_player_num = ((game.current_player_num - 1) % game.num_players()) + 1

                            # Change next_player value too
                            next_player = game.players.filter(
                                "player_num =",
                                game.current_player_num).get().user.username

                        # Create a history step for game.
                        step = HistoryStep(
                            game=game,
                            move_num=game.total_moves,
                            player_name=expected_player.user.username,
                            roll_value=dice_roll,
                            new_pos=new_position,
                            hit_snake=hit_snake,
                            hit_ladder=hit_ladder
                        )

                        success = True

                        expected_player.save()
                        game.save()
                        step.save()

        return PlayTurnResponse(
            success=success,
            events=json.dumps(events),
            roll=dice_roll,
            new_position=new_position,
            next_player=next_player)


    @endpoints.method(
        REQUEST_START_GAME, StartGameResponse, http_method='POST',
        path="startGame", name="startGame")
    def start_game(self, request):

        success = False
        events = []
        next_player = None

        game = db.GqlQuery(
            "SELECT * FROM SnakesAndLaddersGame WHERE game_name = :1",
            request.game_name.lower()).get()

        if game is None:
            events.append(
                "Game does not exist! (" + request.game_name.lower() + ")")

        elif game.num_players() == 0:
            events.append("No players have been added to this game.")
        elif game.game_state != "created":
            events.append("This game has already been started.")
        else:

            # Get the name of the current player whose turn it is.
            next_player = game.players.filter(
                "player_num =", game.current_player_num).get().user.username

            game.game_state = "playing"
            game.save()

            events.append(
                "Game starting with " + str(game.num_players()) + " players.")

            success = True

        return StartGameResponse(
            success=success,
            events=str(events),
            next_player=next_player)

APPLICATION = endpoints.api_server([SnakesAndLaddersAPI])
