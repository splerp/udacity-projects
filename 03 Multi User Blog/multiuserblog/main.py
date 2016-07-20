import webapp2
import jinja2

from google.appengine.ext import db

import src.security as security
from src.route import Handler
from src.data import SiteUser, BlogPost, BlogPostReaction
import src.data as data
import src.dbextensions as dbExtensions

### Cookies
# self.response.headers.add_header('Set-Cookie', 'user_name=%s' % "Override.")
# user_name = self.request.cookies.get('user_name', 'Guest') + " asd."

def get_current_username(cookies):
    return security.cookie_value(cookies.get('user_name', None))

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
        self.render("entry_new.html", True, new_id = None)
        
    def post(self):
        title, summary, contents = self.getThese("entry_title", "entry_summary", "entry_contents")
        
        user_name = get_current_username(self.request.cookies)
        error_messages = validate_blog_post(title, summary, contents, user_name)
        
        new_id = None
        
        if len(error_messages) == 0:
            
            post = BlogPost(
                title = title,
                owner = user_name,
                contents = contents,
                summary = summary)
            post.put()
            new_id = post.key()
        
        self.render("entry_new.html", True, new_id = new_id, error_messages = error_messages)

class EditEntryHandler(Handler):
    def get(self, post_k):
        self.render("entry_edit.html", True, post = db.get(post_k))
        
    def post(self, post_k):
    
        post = db.get(post_k)
    
        title, contents = self.getThese("entry_title", "entry_contents")
        
        post.title = title
        post.contents = contents
        post.put()
        
        self.render("entry_new.html", True, post = db.get(post_k))

import json

class LikePostHandler(Handler):

    def get(self, post_k):
        
        # Will be returning JSON.
        self.response.headers['Content-Type'] = 'application/json'   
        
        # Find entry for current user.
        user_name = get_current_username(self.request.cookies)
        query = db.GqlQuery("SELECT * FROM SiteUser WHERE username = :1", user_name)
        user_k = query.get().key()
        
        # Find reaction type.
        reaction_type = self.getThese("reaction_type")
        
        # Create new reaction entry.
        post_reaction = BlogPostReaction(
            blog_post = db.get(post_k),
            site_user = user.key(),
            reaction_type = reaction_type)
        post_reaction.put()
        post_reaction_k = post_reaction.key()
        
        # Generate data to return and return it.
        obj = {'success': True} 
        self.response.out.write(json.dumps(obj))

    def post(self, post_k):
        
        # Will be returning JSON.
        self.response.headers['Content-Type'] = 'application/json'   
        
        # Find entry for current user.
        user_name = get_current_username(self.request.cookies)
        query = db.GqlQuery("SELECT * FROM SiteUser WHERE username = :1", user_name)
        user_k = query.get().key()
        
        # Find reaction type.
        (reaction_type, ) = self.getThese("reaction_type")
        
        # Create new reaction entry.
        post_reaction = BlogPostReaction(
            blog_post = db.get(post_k),
            site_user = user_k,
            reaction_type = reaction_type)
        post_reaction.put()
        post_reaction_k = post_reaction.key()
        
        # Generate data to return and return it.
        obj = {'success': True} 
        self.response.out.write(json.dumps(obj))
        

class DeleteEntryHandler(Handler):
    def get(self, post_k):
        
        self.response.delete_cookie('user_name')
        self.redirect("/")

class MembersHandler(Handler):
    def get(self):
    
        users = db.GqlQuery("SELECT * FROM SiteUser ORDER BY username")
        self.render("members.html", users = users)

class FizzbuzzHandler(Handler):
    def get(self):
        self.render("fizzbuzz.html")

class AdminHandler(Handler):
    def get(self):
        self.render("admin.html", True)
        
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
        
        self.render("admin.html", True)

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
                self.response.headers.add_header('Set-Cookie', str('user_name=%s' % security.make_cookie_data(name.lower())))
                
                # Return to main page.
                self.redirect("/")
                
        
        self.render("login.html", error_messages = error_messages, form_user_name = name)

class LogoutHandler(Handler):
    def get(self):
        
        self.response.delete_cookie('user_name')
        self.redirect("/")
        
class RegisterHandler(Handler):
    def get(self):
        
        self.render("register.html", new_id = None)
        
    def post(self):
    
        name, pass1, pass2, email = self.getThese("register-name", "register-pass1", "register-pass2", "register-email");
    
        error_messages = validate_register(name, pass1, pass2, email)
        
        new_id = None
        
        if len(error_messages) == 0:
            user = SiteUser(
                username = name.lower(),
                password = security.make_pw_hash(name, pass1, security.make_salt()),
                email = email)
            user.put()
            new_id = user.key()
            
        self.render("register.html", new_id = new_id, error_messages = error_messages, form_user_name = name, form_email = email)
        

#############################
# Authentication Validation #

def validate_register(username, password, password2, email):
    
    errors = []
    
    if len(username) == 0:
        errors.append("Username is required.")
        
    if password != password2:
        errors.append("Passwords must match.")
    else:
        if len(password) == 0:
            errors.append("Password is required.")
            
        if len(password2) == 0:
            errors.append("Password confirmation is required.")
    
    return errors
    
def validate_login(username, password):
    
    errors = []
    
    if len(username) == 0:
        errors.append("Username is required.")
        
    if len(password) == 0:
        errors.append("Password is required.")
    
    return errors

def validate_blog_post(title, summary, contents, user_name):
    
    errors = []
    
    if user_name is None:
        errors.append("You must be logged in to create a blog post.")
    
    else:
        if len(title) == 0:
            errors.append("Title is required.")
            
        if len(contents) == 0:
            errors.append("Summary is required.")
    
    return errors

 
def attempt_user_login(username, password):
    
    errors = []
    valid = False
    
    user = dbExtensions.get_user_from_username(username)
    
    if user is None:
        errors.append("No user could be found with this username.")
    else:
        if security.valid_pw(username, password, user.password):
            valid = True
        else:
            errors.append("The password for this user is incorrect.")
            
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
    ('/logout', LogoutHandler),
    ('/likepost/(.+)', LikePostHandler)
], debug=True)






















    
   
  
 




















