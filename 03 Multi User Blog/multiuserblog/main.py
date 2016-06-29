
import webapp2
import jinja2

from google.appengine.ext import db

import src.security
from src.route import Handler

class IndexHandler(Handler):
    def get(self):
        items = self.request.get_all("food")
        self.render("shopping.html", items=items)

class FizzbuzzHandler(Handler):
    def get(self):
        self.render("fizzbuzz.html")

class LoginHandler(Handler):
    def get(self):
        self.render("login.html")
        
    def post(self):
        error_messages = ["No", "no", "none of that"]
        self.render("login.html", error_messages = error_messages)

class RegisterHandler(Handler):
    def get(self):
        
        users = db.GqlQuery("SELECT * FROM SiteUser ORDER BY username")
        self.render("register.html", users=users)
        
    def post(self):
    
        error_messages = validate_register(
            self.request.get("register-name"),
            self.request.get("register-pass1"),
            self.request.get("register-pass2"),
            self.request.get("register-email"))
        
        if len(error_messages) == 0:
            user = SiteUser(
                username = self.request.get("register-name"),
                password = self.request.get("register-pass1"),
                email = self.request.get("register-email"))
            user.put()
            
        users = db.GqlQuery("SELECT * FROM SiteUser ORDER BY username")
        self.render("register.html", users=users, error_messages = error_messages)
        
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/fizzbuzz', FizzbuzzHandler),
    ('/register', RegisterHandler),
    ('/login', LoginHandler)
], debug=True)

#Integer, Float, String, Date, Time, DateTime, Email, Link, PostalAddress

# A DB entity
class SiteUser(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()
    description = db.TextProperty()
    joindate = db.DateTimeProperty(auto_now_add = True)


months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day

def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year < 2020:
            return year


def validate_register(username, password, password2, email):
    
    errors = []
    
    if len(username) == 0:
        errors.append("Username is required.")
    elif len(username) > 10:
        errors.append("Username cannot be longer than 10 characters.")

    if password != password2:
        errors.append("Passwords must match.")
        
    if(email == "dog"):
        errors.append("no")
    
    return errors
    









































