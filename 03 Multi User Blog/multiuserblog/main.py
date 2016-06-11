
import webapp2
import jinja2

import src.security
from src.route import Handler

class IndexHandler(Handler):
    def get(self):
        self.render("base.html")
        
app = webapp2.WSGIApplication([
    ('/', IndexHandler)
], debug=True)
