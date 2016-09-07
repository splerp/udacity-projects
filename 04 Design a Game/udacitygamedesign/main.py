#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""

import ast
import json
import webapp2
import endpoints
from google.appengine.api import mail, app_identity
from google.appengine.ext import db

import src.security as security
from src.route import Handler
from src.data import (SiteUser, SnakesAndLaddersGame, UserGame,
                      convert_string_to_board)
from src.auth import LoginHandler, LogoutHandler, RegisterHandler
from src.game_api import (SnakesAndLaddersAPI, REQUEST_CREATE_GAME_CONTAINER,
                          REQUEST_EMPTY)
from src.dbextensions import get_rankings


def get_current_username(cookies):
    return security.cookie_value(cookies.get('user_name', None))


def get_user_entity_from_username(user_name):
    query = db.GqlQuery(
        "SELECT * FROM SiteUser WHERE username = :1",
        user_name)
    return query.get()


class IndexHandler(Handler):
    """Handler for the landing page of the website."""

    def get(self):

        user_name = get_current_username(self.request.cookies)
        user = get_user_entity_from_username(user_name)

        # Get the associated game for each UserGame entry for this user.
        all_games = []
        if user is not None:
            all_games = [game.game for game in user.games if (
                game.game.game_state == "playing" or
                game.game.game_state == "created")]

        self.render(
            "index.html",
            user_games=all_games
        )


class GameListHandler(Handler):
    """
    Handler for the games page, which lists all currently
    open games for joining.
    """

    def get(self):

        user_name = get_current_username(self.request.cookies)
        user = get_user_entity_from_username(user_name)
        user_games = [usergame.game.game_name for usergame in user.games]

        all_games = SnakesAndLaddersGame.all().filter(
            "game_state =", "created")

        # Remove any games this player is already in.
        filtered = [game for game in all_games if (
            game.game_name not in user_games)]

        self.render(
            "games.html",
            games=filtered
        )


class CreateGameHandler(Handler):
    """Handler for the create game page."""

    def get(self):

        self.render(
            "games-add.html", True,
            success=True,
            events=[]
        )

    def post(self):

        (title, ) = self.getThese("game-name")

        user_name = get_current_username(self.request.cookies)
        user = get_user_entity_from_username(user_name)

        # Call API.
        api = SnakesAndLaddersAPI()
        container = REQUEST_CREATE_GAME_CONTAINER.combined_message_class(
            game_name=title)
        response = api.create_game(container)

        if response.success:
            new_game = db.get(response.game_key)

            # Automatically add the current user to the game too.
            newUserGame = UserGame(
                user=user,
                game=new_game,
                player_num=1,
                is_owner=True)
            newUserGame.save()

            self.redirect("/games/" + str(new_game.key()))

        self.render(
            "games-add.html",
            game_name=title,
            success=response.success,
            events=ast.literal_eval(response.events)
        )


class GameListMineHandler(Handler):
    """
    Handler for the games page, which lists all
    currently open games for joining.
    """

    def get(self):

        user_name = get_current_username(self.request.cookies)
        user = get_user_entity_from_username(user_name)

        # Get the associated game for each UserGame entry for this user.
        all_games = []
        if user is not None:
            all_games = [game.game for game in user.games if (
                game.game.game_state == "playing" or
                game.game.game_state == "created")]

        self.render(
            "games-mine.html", True,
            user_games=all_games
        )


class LeaderboardHandler(Handler):
    """Retrieves all leaderboard data."""

    def get(self):

        self.render(
            "leaderboard.html",
            rankings=get_rankings()
        )


class GameHandler(Handler):
    """
    Handler for the games page, which lists all
    currently open games for joining.
    """

    def get(self, game_k):

        game = db.get(game_k)

        self.render(
            "game.html",
            True,
            game=game,
            game_board=json.dumps(
                convert_string_to_board(game.game_board).__dict__)
        )


class GameInfoHandler(Handler):
    """
    Handler for the games page, which lists
    all currently open games for joining.
    """

    def get(self, game_k):

        game = db.get(game_k)

        # Will be returning JSON.
        self.response.headers['Content-Type'] = 'application/json'

        current_player = game.players.filter(
            "player_num =", game.current_player_num).get()

        # Generate data to return and return it.
        obj = {'success': True,
               'game_state': game.game_state,
               'num_players': game.num_players(),
               'owner': game.get_owner(),
               'player_data': [{"name": player.user.username,
                                "position": player.position,
                                "player_num": player.player_num}
                               for player in game.players],
               'current_player_num': game.current_player_num,
               'current_player_name': (
                    current_player.user.username if current_player is not None
                    else "")}

        self.response.out.write(json.dumps(obj))


class WelcomeHandler(Handler):
    """Handler for the welcome page shown when registering / logging in."""

    def get(self):

        (action, ) = self.getThese("action")

        if not security.is_logged_in(self.request):
            self.redirect("/")
        else:
            # Customise welcome message to be relevent to user's origin
            self.render(
                "welcome.html",
                action_name=(
                    "logging in" if action == "login"
                    else "registering")
                )


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""

        app_id = app_identity.get_application_id()
        users = SiteUser.all()

        num_created = 1

        for user in users:
            if user.email is not None and user.email != "":
                for usergame in user.games:

                    should_send_email = False

                    subject = ""
                    body = ""

                    username = user.username
                    gamename = usergame.game.game_name

                    if usergame.game.game_state == "created":
                        should_send_email = True
                        subject = ("Reminder: You haven't started playing" +
                                   " your snakes and ladders game! " +
                                   str(num_created))
                        body = ("Hi there " + username + ". Please view your" +
                                " game " + gamename + " and get some people " +
                                "playing.")

                    elif (usergame.game.game_state == "playing" and
                          (usergame.player_num ==
                           usergame.game.current_player_num)):
                        should_send_email = True
                        subject = ("Reminder: Keep playing snakes and" +
                                   " ladders! You have an unfinished game. " +
                                   str(num_created))
                        body = ("Hi there " + username + ". Please view your" +
                                " game " + gamename + " and play your turn.")

                    if should_send_email:
                        num_created += 1
                        # This will send test emails:
                        # from, to, subject, body
                        mail.send_mail(
                            'noreply@{}.appspotmail.com'.format(app_id),
                            user.email,
                            subject,
                            body)

        self.response.set_status(204)


class EmailGameJoin(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache FIIIIX."""

        app_id = app_identity.get_application_id()

        user_k = db.Key(self.request.get('user'))
        user = db.get(user_k)

        if user.email is not None and user.email != "":
            email_to = user.email
            email_from = 'noreply@{}.appspotmail.com'.format(app_id)
            game_name = self.request.get("game_name")

            subject = (
                "You have joined {}: Snakes and Ladders".format(game_name))
            body = ("Hi {}! You are now part of a game of snakes and ladders" +
                    ". Room name is {}.".format(user.username, game_name))

            mail.send_mail(
                email_from,
                email_to,
                subject,
                body)

        self.response.set_status(204)


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/welcome', WelcomeHandler),
    ('/register', RegisterHandler),
    ('/games', GameListHandler),
    ('/games/add', CreateGameHandler),
    ('/games/mine', GameListMineHandler),
    ('/games/leaderboard', LeaderboardHandler),
    ('/games/(.+)/getdata', GameInfoHandler),
    ('/games/(.+)', GameHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/crons/send_test_cron', SendReminderEmail),
    ('/tasks/email_game_join', EmailGameJoin),
], debug=True)
