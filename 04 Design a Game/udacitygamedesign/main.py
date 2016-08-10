#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""

import webapp2
from google.appengine.api import mail, app_identity

from data import SiteUser
from game_api import SnakesAndLaddersAPI


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        users = SiteUser.all()
        
        for user in users:
            for usergame in user.games:
                if usergame.game.game_state == "created":
                    subject = "Stale game detected."
                    body = "FIX IT."

                    # This will send test emails, the arguments to send_mail are:
                    # from, to, subject, body
                    mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                                   user.email,
                                   subject,
                                   body)


        self.response.set_status(204)

class SendInvitation(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""

        app_id = app_identity.get_application_id()

        # TODO pass in user name instead to retrieve name and email and etc.

        email_to = self.request.get("email")
        email_from = 'noreply@{}.appspotmail.com'.format(app_id)
        game_name = self.request.get("game_name")

        subject = "Join me in the {} room ;3;3;3".format(game_name)
        body = "Hi! You've been invited to join someone in a game of snakes and ladders. Room name is {}.".format(game_name)

        # This will send test emails, the arguments to send_mail are:
        # from, to, subject, body
        mail.send_mail(
            email_from,
            email_to,
            subject,
            body)

        self.response.set_status(204)


app = webapp2.WSGIApplication([
    ('/crons/send_test_cron', SendReminderEmail),
    ('/tasks/send_invite_email', SendInvitation),
], debug=True)
