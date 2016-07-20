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


def get_user_entity_from_username(user_name):
    query = db.GqlQuery("SELECT * FROM SiteUser WHERE username = :1", user_name)
    return query.get()


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
        user = get_user_entity_from_username(user_name)
        
        error_messages = validate_blog_post(title, summary, contents, user_name)
        
        new_id = None
        
        if len(error_messages) == 0:
            
            post = BlogPost(
                title = title,
                owner = user,
                contents = contents,
                summary = summary)
            post.put()
            new_id = post.key()
        
        self.render("entry_new.html", True, new_id = new_id, error_messages = error_messages)

class EditEntryHandler(Handler):
    def get(self, post_k):
        self.render("entry_edit.html", True, post = db.get(post_k))
        
    def post(self, post_k):
    
        submitted = False
        post = db.get(post_k)
    
        title, summary, contents = self.getThese("entry-title", "entry-summary", "entry-contents")
        
        # Find entry for current user.
        user_name = get_current_username(self.request.cookies)
        current_user = get_user_entity_from_username(user_name)
        
        error_messages = []
        
        if post.owner.key() == current_user.key():
        
            error_messages = validate_blog_post(title, summary, contents, user_name)
            
            if len(error_messages) == 0:
                post.title = title
                post.contents = contents
                post.put()
                submitted = True
        else:
            error_messages.append("You cannot edit someone else's blog post!")
        
        self.render("entry_edit.html", True, submitted = submitted, post = post, error_messages = error_messages)

import json

class LikePostHandler(Handler):

    def post(self, post_k):
        
        reaction_already_exists = False
        deleted = False
        
        # Will be returning JSON.
        self.response.headers['Content-Type'] = 'application/json'   
        
        # Find entry for current user.
        user_k = get_user_entity_from_username(get_current_username(self.request.cookies)).key()
        
        # Find reaction type.
        (reaction_type, ) = self.getThese("reaction_type")
        
        query = db.GqlQuery("SELECT * FROM BlogPostReaction WHERE blog_post = :1 AND site_user = :2",
            db.get(post_k),
            db.get(user_k))
        
        old_reaction = query.get()
        
        # Check if this value should be removed instead.
        if reaction_type == "":
            if old_reaction is not None:
                old_reaction.delete()
                reaction_already_exists = True
                deleted = True
        else:
            if old_reaction is not None:
                old_reaction.reaction_type = reaction_type
                old_reaction.put()
                reaction_already_exists = True
            else:
                # Create new reaction entry.
                post_reaction = BlogPostReaction(
                    blog_post = db.get(post_k),
                    site_user = db.get(user_k),
                    reaction_type = reaction_type)
                post_reaction.put()
                reaction_already_exists = False
        
        # Generate data to return and return it.
        obj = {'success': True,
               'alreadyExists': reaction_already_exists,  # Added vote, or removed vote.
               'deleted': deleted}

        self.response.out.write(json.dumps(obj))
        
class LikePostCheckHandler(Handler):

    def post(self, post_k):
        
        # Will be returning JSON.
        self.response.headers['Content-Type'] = 'application/json'   
        
        # Find entry for current user.
        user_k = get_user_entity_from_username(get_current_username(self.request.cookies)).key()
        
        query = db.GqlQuery("SELECT * FROM BlogPostReaction WHERE blog_post = :1 AND site_user = :2",
            db.get(post_k),
            db.get(user_k))
        
        old_reaction = query.get()
        
        current_value = ""
        if old_reaction is not None:
            current_value = old_reaction.reaction_type
        
        # Generate data to return and return it.
        obj = {'success': True,
               'value': current_value}

        self.response.out.write(json.dumps(obj))
        

class DeleteEntryHandler(Handler):
    def post(self, post_k):
        
        if db.get(post_k) is not None:
            db.get(post_k).delete()

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
            
        if len(summary) == 0:
            errors.append("Summary is required.")
            
        if len(contents) == 0:
            errors.append("Contents is required.")
    
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
    ('/blog/delete/(.+)', DeleteEntryHandler),
    ('/blog/(.+)', BlogEntryHandler),
    ('/members', MembersHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/likepost/(.+)', LikePostHandler),
    ('/likepostcheck/(.+)', LikePostCheckHandler)
], debug=True)






















    
   
  
 




















