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

    game_state = db.StringProperty(required=True,
                                   choices=('created', 'playing', 'cancelled', 'complete'),
                                   default='created')
                                   
    num_players = db.IntegerProperty(default=0)
    current_player_num = db.IntegerProperty(default=0)

    total_moves = db.IntegerProperty(default=0)
    ladders_hit = db.IntegerProperty(default=0)
    snakes_hit = db.IntegerProperty(default=0)


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

    position = db.IntegerProperty(default=0)
    is_winner = db.BooleanProperty(default=False)

class Score(db.Model):

    user = db.ReferenceProperty(SiteUser,
                                required=True,
                                collection_name='scores')

    game = db.ReferenceProperty(SnakesAndLaddersGame,
                                required=True,
                                collection_name='scores')
