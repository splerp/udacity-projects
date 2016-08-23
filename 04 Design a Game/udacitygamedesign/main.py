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
from src.data import SiteUser, SnakesAndLaddersGame, UserGame
from src.auth import LoginHandler, LogoutHandler, RegisterHandler
from src.game_api import SnakesAndLaddersAPI, REQUEST_CREATE_GAME_CONTAINER

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
            all_games = [game.game for game in user.games]

        self.render(
            "index.html",
            user_games=all_games
        )

class GameListHandler(Handler):
    """Handler for the games page, which lists all currently open games for joining."""

    def get(self):

        all_games = SnakesAndLaddersGame.all().filter("game_state =", "created")

        self.render(
            "games.html",
            games=all_games
        )

class CreateGameHandler(Handler):
    """Handler for the create game page."""

    def get(self):

        self.render(
            "games-add.html",
            success=True,
            events=[]
        )

    def post(self):

        (title, ) = self.getThese("game-name")

        user_name = get_current_username(self.request.cookies)
        user = get_user_entity_from_username(user_name)

        # Call API.
        api = SnakesAndLaddersAPI()
        container = REQUEST_CREATE_GAME_CONTAINER.combined_message_class(game_name=title)
        response = api.create_game(container)

        new_game = SnakesAndLaddersGame.all().filter("game_name =", title.lower()).get()

        print "new_game***************", new_game

        # Automatically add the current user to the game too.
        newUserGame = UserGame(user=user, game=new_game, player_num=1)
        newUserGame.save()

        self.redirect("/games/" + str(new_game.key()))

        self.render(
            "games-add.html",
            game_name=title,
            success=response.success,
            events=ast.literal_eval(response.events)
        )


class GameListMineHandler(Handler):
    """Handler for the games page, which lists all currently open games for joining."""

    def get(self):

        user_name = get_current_username(self.request.cookies)
        user = get_user_entity_from_username(user_name)

        # Get the associated game for each UserGame entry for this user.
        all_games = []
        if user is not None:
            all_games = [game.game for game in user.games]

        self.render(
            "games-mine.html", True,
            user_games=all_games
        )

class GameHandler(Handler):
    """Handler for the games page, which lists all currently open games for joining."""

    def get(self, game_k):

        game = db.get(game_k)

        self.render(
            "game.html", True,
            game=game
        )

class GameInfoHandler(Handler):
    """Handler for the games page, which lists all currently open games for joining."""

    def get(self, game_k):

        game = db.get(game_k)

        # Will be returning JSON.
        self.response.headers['Content-Type'] = 'application/json'

        current_player = game.players.filter("player_num =", game.current_player_num).get()

        # Generate data to return and return it.
        obj = {'success': True,
               'game_state': game.game_state,
               'num_players': game.num_players,
               'player_data': [{"name" : player.user.username, "position" : player.position, "player_num" : player.player_num} for player in game.players],
               'current_player_num': game.current_player_num,
               'current_player_name': current_player.user.username if current_player is not None else ""}

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


class MembersHandler(Handler):
    def get(self):

        users = db.GqlQuery("SELECT * FROM SiteUser ORDER BY username")
        self.render("members.html", users=users)

class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        users = SiteUser.all()
        
        num_created = 1
        
        for user in users:
            for usergame in user.games:
            
                should_send_email = False
            
                subject = ""
                body = ""
            
                if usergame.game.game_state == "created":

                    should_send_email = True
                    subject = "Reminder: You haven't started playing your snakes and ladders game! " + str(num_created)
                    body = "FIX IT."
                    
                elif usergame.game.game_state == "playing":

                    should_send_email = True
                    subject = "Reminder: Keep playing snakes and ladders! You have an unfinished game. " + str(num_created)
                    body = "FIX IT."
                                   
                if should_send_email:
                    num_created += 1
                    # This will send test emails, the arguments to send_mail are:
                    # from, to, subject, body
                    mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
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
        email_to = user.email
        email_from = 'noreply@{}.appspotmail.com'.format(app_id)
        game_name = self.request.get("game_name")

        subject = "You have joined {}: Snakes and Ladders".format(game_name)
        body = "Hi {}! You are now part of a game of snakes and ladders. Room name is {}.".format(user.username, game_name)

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
    ('/members', MembersHandler),
    ('/games', GameListHandler),
    ('/games/add', CreateGameHandler),
    ('/games/mine', GameListMineHandler),
    ('/games/(.+)/getdata', GameInfoHandler),
    ('/games/(.+)', GameHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/crons/send_test_cron', SendReminderEmail),
    ('/tasks/email_game_join', EmailGameJoin),
], debug=True)