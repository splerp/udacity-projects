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

    position_p1 = db.IntegerProperty(required=True, default=0)
    position_p2 = db.IntegerProperty(required=True, default=0)

    game_state = db.StringProperty(required=True,
                                   choices=('created', 'turn_p1', 'turn_p2', 'cancelled', 'complete'),
                                   default='created')

    # Also, inherits 'users'.



class UserGame(db.Model):

    user = db.ReferenceProperty(SiteUser,
                                required=True,
                                collection_name='games')

    game = db.ReferenceProperty(SnakesAndLaddersGame,
                                required=True,
                                collection_name='users')

class Score(db.Model):

    user = db.ReferenceProperty(SiteUser,
                                required=True,
                                collection_name='scores')

    game = db.ReferenceProperty(SnakesAndLaddersGame,
                                required=True,
                                collection_name='scores')
