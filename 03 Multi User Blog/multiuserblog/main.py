
import webapp2
import jinja2

from google.appengine.ext import db

import src.security
from src.route import Handler

class IndexHandler(Handler):
    def get(self):
        self.render("landing.html")

class BlogHandler(Handler):
    def get(self):
    
        tmp = BlogPost(
            blog_post_id = 1,
            title = "Test 1",
            owner = "tester",
            contents = "asdniaw oaw djioaw djawodawjdaiwdoaiw djaw dijaw d aoi daw oji dawojida wdja woidja wiodjaiw doawjd iawd ja  d oaw j ji jawd j")
        tmp.put()
    
        blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY date_posted")
        self.render("blog.html", blog_posts=blog_posts)

class NewEntryHandler(Handler):
    def get(self):
        self.render("newentry.html")

class PostHandler(Handler):
    def get(self):
    
        tmp = BlogPost(
            blog_post_id = 1,
            title = "Test 1",
            owner = "tester",
            contents = "asdniaw oaw djioaw djawodawjdaiwdoaiw djaw dijaw d aoi daw oji dawojida wdja woidja wiodjaiw doawjd iawd ja  d oaw j ji jawd j")
        tmp.put()
        
        #id = self.request.get("id") if self.request.get("id") is not null else 1;
        id = 1;
    
        self.render("post.html", post = db.GqlQuery("SELECT * FROM BlogPost WHERE blog_post_id = " + "1")[0])

class MembersHandler(Handler):
    def get(self):
    
        users = db.GqlQuery("SELECT * FROM SiteUser ORDER BY username")
        self.render("members.html", users = users)

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
        
        self.render("register.html")
        
    def post(self):
    
        name, pass1, pass2, email = self.getThese("register-name", "register-pass1", "register-pass2", "register-email");
    
        error_messages = validate_register(name, pass1, pass2, email)
        
        if len(error_messages) == 0:
            user = SiteUser(
                username = name,
                password = pass1,
                email = email)
            user.put()
            
        self.render("register.html", error_messages = error_messages)
        
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/fizzbuzz', FizzbuzzHandler),
    ('/register', RegisterHandler),
    ('/blog', BlogHandler),
    ('/newentry', NewEntryHandler),
    ('/post', PostHandler),
    ('/members', MembersHandler),
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

# A DB entity
class BlogPost(db.Model):
    blog_post_id = db.IntegerProperty()
    title = db.StringProperty(required = True)
    owner = db.StringProperty(required = True)
    contents = db.TextProperty(required = True)
    likes = db.IntegerProperty()
    date_posted = db.DateTimeProperty(auto_now_add = True)


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
    









































