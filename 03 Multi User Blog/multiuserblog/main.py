import webapp2
import jinja2

from google.appengine.ext import db

import src.security as security
from src.route import Handler
from src.data import SiteUser, BlogPost
import src.data as data
import src.dbextensions as dbExtensions

### Cookies
# self.response.headers.add_header('Set-Cookie', 'user_name=%s' % "Override.")
# user_name = self.request.cookies.get('user_name', 'Guest') + " asd."

class IndexHandler(Handler):
    def get(self):
        
        self.render("landing.html")

class BlogHandler(Handler):
    def get(self):
    
        blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY date_posted")
        
        self.render("blog.html", blog_posts = blog_posts)

class BlogEntryHandler(Handler):
    def get(self, post_k):
    
        self.render("post.html", post = db.get(post_k))

class NewEntryHandler(Handler):
    def get(self):
        self.render("entry_new.html")
        
    def post(self):
        title, summary, contents = self.getThese("entry_title", "entry_summary", "entry_contents")
        user_name = self.request.cookies.get('user_name', None)
        
        
        post = BlogPost(
            title = title,
            owner = user_name,
            contents = contents,
            summary = summary)
        post.put()
        
        self.render("entry_new.html", new_id = post.key())

class EditEntryHandler(Handler):
    def get(self, post_k):
        self.render("entry_edit.html", post = db.get(post_k))
        
    def post(self, post_k):
    
        post = db.get(post_k)
    
        title, contents = self.getThese("entry_title", "entry_contents")
        
        post.title = title
        post.contents = contents
        post.put()
        
        self.render("entry_new.html", post = db.get(post_k))

class MembersHandler(Handler):
    def get(self):
    
        users = db.GqlQuery("SELECT * FROM SiteUser ORDER BY username")
        self.render("members.html", users = users)

class FizzbuzzHandler(Handler):
    def get(self):
        self.render("fizzbuzz.html")

class AdminHandler(Handler):
    def get(self):
        self.render("admin.html")
        
    def post(self):
        delete_users, delete_posts = self.getThese("delete_users", "delete_posts")
        
        if delete_users is not None:
            users = db.GqlQuery("SELECT * FROM SiteUser")
            for user in users:
                user.delete()
            
        if delete_posts is not None:
            posts = db.GqlQuery("SELECT * FROM BlogPost")
            for post in posts:
                post.delete()
        
        self.render("admin.html")

#######################
# User Authentication #

class LoginHandler(Handler):
    def get(self):
        self.render("login.html")
        
    def post(self):
        
        name, password = self.getThese("login-name", "login-password");
        
        error_messages = validate_login(name, password)
        
        if len(error_messages) == 0:
        
            error_messages, result = attempt_user_login(name, password)
            
            if result:
            
                # Set current user cookie.
                self.response.headers.add_header('Set-Cookie', str('user_name=%s' % security.make_cookie_value(name.lower())))
                
                self.redirect("/")
                
        
        self.render("login.html", error_messages = error_messages)

class LogoutHandler(Handler):
    def get(self):
        
        self.response.delete_cookie('user_name')
        self.redirect("/")
        
class RegisterHandler(Handler):
    def get(self):
        
        self.render("register.html")
        
    def post(self):
    
        name, pass1, pass2, email = self.getThese("register-name", "register-pass1", "register-pass2", "register-email");
    
        error_messages = validate_register(name, pass1, pass2, email)
        
        if len(error_messages) == 0:
            user = SiteUser(
                username = name.lower(),
                password = security.make_pw_hash(name, pass1, security.make_salt()),
                email = email)
            user.put()
            
        self.render("register.html", error_messages = error_messages)
        

#############################
# Authentication Validation #

def validate_register(username, password, password2, email):
    
    errors = []
    
    if len(username) == 0:
        errors.append("Username is required.")
    elif len(username) > 10:
        errors.append("Username cannot be longer than 10 characters.")

    if password != password2:
        errors.append("Passwords must match.")
    
    return errors
    
def validate_login(username, password):
    
    errors = []
    
    if len(username) == 0:
        errors.append("Username is required.")
        
    if len(password) == 0:
        errors.append("Password is required.")
    
    return errors

 
def attempt_user_login(username, password):
    
    errors = []
    valid = False
    
    user = dbExtensions.get_user_from_username(username)
    
    if user is None:
        errors.append("No user matches this username")
    else:
        if security.valid_pw(username, password, user.password):
            valid = True
        else:
            errors.append("No user matches this username or password.")
            
    return errors, valid


###################
# Routing Details #

app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/admin', AdminHandler),
    ('/fizzbuzz', FizzbuzzHandler),
    ('/register', RegisterHandler),
    ('/blog', BlogHandler),
    ('/blog/add', NewEntryHandler),
    ('/blog/edit/(.+)', EditEntryHandler),
    ('/blog/(.+)', BlogEntryHandler),
    ('/members', MembersHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler)
], debug=True)






















    
   
  
 




















