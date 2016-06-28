
import webapp2
import jinja2

import src.security
from src.route import Handler

class IndexHandler(Handler):
    def get(self):
        self.render("shopping.html")

class FizzbuzzHandler(Handler):
    def get(self):
        self.render("fizzbuzz.html")

        
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/fizzbuzz', FizzbuzzHandler),
], debug=True)


33 27