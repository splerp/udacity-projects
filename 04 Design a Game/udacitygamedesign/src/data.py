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
    
    def get_owner(self):
        
        # Find a matching player.
        for player in self.players:
            if player.is_owner:
                return player.user.username
    
        return ""
    
    def get_summary(self):
        
        summary = ""
        nametxt = "No players"
    
        if self.players.count() > 0:
            names = [str(player.user.username) for player in self.players];
            nametxt = string_commas_and(names)
 
        summary += "{0} are playing. They have hit {1} object{2}.".format(
            nametxt,
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
    is_owner = db.BooleanProperty(default=False)


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


def string_commas_and(to_convert):
    
    to_return = ""
    
    if len(to_convert) > 0:
        # Convert into style x, y, z, and w
        if len(to_convert) > 1:
            for element in to_convert[:-2]:
                to_return += element + ", "
            
            to_return += to_convert[len(to_convert)-2] + " and " + to_convert[len(to_convert)-1]
        # Return first element
        else:
            to_return += to_convert[0]
    
    return to_return

"""default_sal_board = SALBoard(
    size = 100,
    snakes=[(15, 2), (23, 9), (65, 50), (91, 14)],
    ladders=[(5, 20), (6, 50), (61, 87), (43, 97)]
)"""

default_sal_board = SALBoard(
    size = 100,
    snakes=[(4, 2), (12, 9), (62, 19), (70, 28), (72, 23), (85, 14), (98, 91), (99, 5)],
    ladders=[(1, 100), (6, 66), (27, 45), (47, 77), (73, 88), (69, 83)]
)