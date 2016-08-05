"""Hello World API implemented using Google Cloud Endpoints.

Contains declarations of endpoint, endpoint methods,
as well as the ProtoRPC message class and container required
for endpoint method definition.
"""
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from data import SnakesAndLaddersGame, UserGame, SiteUser

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

REQUEST_CREATE_GAME_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    game_name=messages.StringField(1, default="A New Game"),
    player_name_1=messages.StringField(2, required=True),
    player_name_2=messages.StringField(3, required=True), # Make required
)

REQUEST_SITE_USER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    username=messages.StringField(1),
    password=messages.StringField(2),
    email=messages.StringField(3),
    description=messages.StringField(4)
)


class CreateGameResponse(messages.Message):
    """String that stores a message."""
    success = messages.BooleanField(1)
    game_id = messages.StringField(2)
    board = messages.StringField(3)

class KillEverythingResponse(messages.Message):
    success = messages.BooleanField(1)

class CreateSiteUserResponse(messages.Message):
    success = messages.BooleanField(1)
    site_user_id = messages.StringField(2)

@endpoints.api(name='snakesandladdersendpoints', version='v1')
class HelloWorldApi(remote.Service):

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

        return CreateSiteUserResponse(success=True, site_user_id=str(user.key()))

    @endpoints.method(
        REQUEST_EMPTY, KillEverythingResponse, http_method='POST',
        path = "killEverything", name = "killEverything")
    def kill_everything(self, request):

        remove_all_data()

        return KillEverythingResponse(success=True)

    @endpoints.method(
        REQUEST_CREATE_GAME_CONTAINER, CreateGameResponse, http_method='POST',
        path = "createGame", name = "createGame")
    def greeting_by_time(self, request):
        message = "You are starting a new game called {} with players {} and {}".format(
            request.game_name, request.player_name_1, request.player_name_2)

        player1 = db.GqlQuery("SELECT * FROM SiteUser WHERE username = :1", request.player_name_1.lower()).get()
        player2 = db.GqlQuery("SELECT * FROM SiteUser WHERE username = :1", request.player_name_2.lower()).get()


        # Create game with players.
        game = SnakesAndLaddersGame(
            game_name = request.game_name,
            game_board = convert_board_to_string(default_sal_board),
        )
        game.save()

        if player1 is None or player2 is None:
            print "COULD NOT FIND BOTH PLAYERS for", request.player_name_1, "and", request.player_name_2

        playerGame1 = UserGame(user=player1, game=game)
        playerGame1.save()

        playerGame2 = UserGame(user=player2, game=game)
        playerGame2.save()

        return CreateGameResponse(success=True, game_id=str(game.key()), board=convert_board_to_string(default_sal_board))


APPLICATION = endpoints.api_server([HelloWorldApi])

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
    print "ok so far..."
    for snake_str in snakes_str:
        if snake_str != '':
            (x, y) = snake_str.split(',')
            print "Adding a snake", (x, y)
            snakes.append((int(x), int(y)))
    ladders = []
    ladders_str = ladders_str.split('.')
    for ladder_str in ladders_str:
        if ladder_str != '':
            (x, y) = ladder_str.split(',')
            print "Adding a ladder", (x, y)
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