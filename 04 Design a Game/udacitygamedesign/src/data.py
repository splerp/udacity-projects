from google.appengine.ext import db


class SiteUser(db.Model):
    """Defines a SiteUser to reference registered users."""

    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    description = db.TextProperty()
    joindate = db.DateTimeProperty(auto_now_add=True)


class SnakesAndLaddersGame(db.Model):

    game_name = db.StringProperty(required=True)
    game_board = db.TextProperty(required=True)

    game_state = db.StringProperty(
        required=True,
        choices=('created', 'playing', 'cancelled', 'complete'),
        default='created')

    #num_players = db.IntegerProperty(default=0)
    current_player_num = db.IntegerProperty(default=0)

    total_moves = db.IntegerProperty(default=0)
    ladders_hit = db.IntegerProperty(default=0)
    snakes_hit = db.IntegerProperty(default=0)

    def num_players(self):
        return self.players.count()
    
    def get_summary(self):
        
        summary = ""
    
        summary += "{0} player{1} hit {2} object{3}.".format(
            self.num_players(),
            " has" if self.num_players() == 1 else "s have",
            self.ladders_hit + self.snakes_hit,
            "" if (self.ladders_hit + self.snakes_hit) == 1 else "s")

        return summary


class HistoryStep(db.Model):

    game = db.ReferenceProperty(SnakesAndLaddersGame,
                                required=True,
                                collection_name='moves')

    move_num = db.IntegerProperty(required=True)

    player_name = db.StringProperty(required=True)
    roll_value = db.IntegerProperty(required=True)
    new_pos = db.IntegerProperty(required=True)

    hit_snake = db.BooleanProperty(required=True)
    hit_ladder = db.BooleanProperty(required=True)


class UserGame(db.Model):

    # Determines which order the players take their turns.
    player_num = db.IntegerProperty(default=0)

    user = db.ReferenceProperty(SiteUser,
                                required=True,
                                collection_name='games')

    game = db.ReferenceProperty(SnakesAndLaddersGame,
                                required=True,
                                collection_name='players')

    position = db.IntegerProperty(default=1)
    is_winner = db.BooleanProperty(default=False)


class Score(db.Model):

    user = db.ReferenceProperty(SiteUser,
                                required=True,
                                collection_name='scores')

    game = db.ReferenceProperty(SnakesAndLaddersGame,
                                required=True,
                                collection_name='scores')


class SALBoard():
    size = 100
    snakes = []
    ladders = []
    def __init__(self, size, snakes, ladders):
        self.size = size
        self.snakes = snakes
        self.ladders = ladders


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
        size=size,
        snakes=snakes,
        ladders=ladders
    )


default_sal_board = SALBoard(
    size = 100,
    snakes=[(15, 2), (23, 9), (65, 50), (91, 14)],
    ladders=[(5, 20), (6, 50), (61, 87), (43, 97)]
)