#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""

import webapp2
from google.appengine.api import mail, app_identity
from google.appengine.ext import db

from data import SiteUser
from game_api import SnakesAndLaddersAPI


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
    ('/crons/send_test_cron', SendReminderEmail),
    ('/tasks/email_game_join', EmailGameJoin),
], debug=True)
