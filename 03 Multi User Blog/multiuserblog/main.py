import webapp2
import json

from google.appengine.ext import db

import src.security as security
from src.route import Handler
from src.data import SiteUser, BlogPost, BlogPostReaction, BlogPostComment
from src.auth import LoginHandler, LogoutHandler, RegisterHandler
from src.validation import validate_blog_post


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

        blog_posts = db.GqlQuery(
            "SELECT * FROM BlogPost ORDER BY date_posted DESC")

        self.render(
            "landing.html",
            blog_posts=blog_posts)


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


class BlogImage(Handler):
    """Code based on content at
    https://cloud.google.com/appengine/docs/python/images/usingimages"""

    def get(self):
        blog_post_k = db.Key(self.request.get('img_id'))
        blog_post = db.get(blog_post_k)

        if blog_post.title_image:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(blog_post.title_image)
        else:
            self.redirect("/content/blank.png")


class BlogHandler(Handler):
    def get(self):

        blog_posts = db.GqlQuery(
            "SELECT * FROM BlogPost ORDER BY date_posted DESC")

        self.render("blog.html", blog_posts=blog_posts)


class BlogEntryHandler(Handler):
    def get(self, post_k):

        self.render("entry_details.html", post=db.get(post_k))

    # Occurs when someone posts a comment.
    def post(self, post_k):

        (title, content) = self.getThese("entry-title", "entry-comment")

        user_name = get_current_username(self.request.cookies)
        user = get_user_entity_from_username(user_name)
        blog_post = db.get(post_k)

        post_comment = BlogPostComment(
            blog_post=blog_post,
            site_user=user,
            title=title,
            content=content)
        post_comment.put()

        self.redirect("/blog/" + post_k)


class NewEntryHandler(Handler):
    def get(self):
        self.render("entry_new.html", True, new_id=None)

    def post(self):
        title, summary, contents, image = self.getThese(
            "entry_title",
            "entry_summary",
            "entry_contents",
            "entry_image")

        user_name = get_current_username(self.request.cookies)
        user = get_user_entity_from_username(user_name)

        # Validate post and retrieve errors.
        error_messages = validate_blog_post(
            title,
            summary,
            contents,
            user_name)

        new_id = None

        if len(error_messages) == 0:

            # Create new blog post.
            post = BlogPost(
                title=title,
                owner=user,
                contents=contents,
                summary=summary,
                title_image=image if image != "" else None)
            post.put()
            new_id = post.key()

        # Render page with all required information.
        self.render(
            "entry_new.html",
            True,
            new_id=new_id,
            error_messages=error_messages,
            entry_title=title,
            entry_summary=summary,
            entry_contents=contents)


class EditEntryHandler(Handler):
    def get(self, post_k):

        post = db.get(post_k)

        self.render(
            "entry_edit.html",
            True,
            post=post,
            entry_title=post.title,
            entry_summary=post.summary,
            entry_contents=post.contents)

    def post(self, post_k):

        submitted = False
        post = db.get(post_k)

        title, summary, contents, image, delete_attachment = self.getThese(
            "entry-title",
            "entry-summary",
            "entry-contents",
            "entry_image",
            "remove-attachment")

        # Find entry for current user.
        user_name = get_current_username(self.request.cookies)
        current_user = get_user_entity_from_username(user_name)

        error_messages = []

        if post.owner.key() == current_user.key():

            # Validate post and return errors.
            error_messages = validate_blog_post(
                title,
                summary,
                contents,
                user_name)

            if len(error_messages) == 0:

                # Update post details.
                post.title = title
                post.summary = summary
                post.contents = contents

                # Only delete the attachment if the delete button was pressed.
                if delete_attachment == "0":
                    post.title_image = image or post.title_image
                else:
                    post.title_image = None

                post.put()
                submitted = True
        else:
            error_messages.append("You cannot edit someone else's blog post!")

        self.render(
            "entry_edit.html",
            True,
            submitted=submitted,
            post=post,
            entry_title=title,
            entry_summary=summary,
            entry_contents=contents,
            error_messages=error_messages)


class LikePostHandler(Handler):
    """Sets the current user's reaction to a post as specified."""

    def post(self, post_k):

        reaction_already_exists = False
        deleted = False

        # Will be returning JSON.
        self.response.headers['Content-Type'] = 'application/json'

        # Find entry for current user.
        user_k = get_user_entity_from_username(
            get_current_username(self.request.cookies)).key()

        # Find reaction type.
        (reaction_type, ) = self.getThese("reaction_type")

        query = db.GqlQuery(
            ("SELECT * FROM BlogPostReaction WHERE "
                "blog_post = :1 AND site_user = :2"),
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
                    blog_post=db.get(post_k),
                    site_user=db.get(user_k),
                    reaction_type=reaction_type)
                post_reaction.put()
                reaction_already_exists = False

        # Generate data to return and return it.
        obj = {'success': True,
               'alreadyExists': reaction_already_exists,
               'deleted': deleted}

        self.response.out.write(json.dumps(obj))


class LikePostCheckHandler(Handler):
    """Returns the current reaction value for a given user on a given post."""

    def get(self, post_k):

        # Will be returning JSON.
        self.response.headers['Content-Type'] = 'application/json'

        # Find entry for current user.
        user_k = get_user_entity_from_username(
            get_current_username(self.request.cookies)).key()

        query = db.GqlQuery(
            ("SELECT * FROM BlogPostReaction "
                "WHERE blog_post = :1 AND site_user = :2"),
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

        post = db.get(post_k)
        user_k = get_user_entity_from_username(
            get_current_username(self.request.cookies)).key()

        # Do not allow deletion unless the current user is the entry owner.
        if user_k == post.owner.key():
            if db.get(post_k) is not None:
                db.get(post_k).delete()
        else:
            self.error(401)


class DeleteCommentHandler(Handler):
    def post(self, comment_k):

        comment = db.get(comment_k)
        user_k = get_user_entity_from_username(
            get_current_username(self.request.cookies)).key()

        # Do not allow deletion unless the current user is the comment owner.
        if user_k == comment.site_user.key():
            if db.get(comment_k) is not None:
                db.get(comment_k).delete()
        else:
            self.error(401)


class MembersHandler(Handler):
    def get(self):

        users = db.GqlQuery("SELECT * FROM SiteUser ORDER BY username")
        self.render("members.html", users=users)


class AdminHandler(Handler):
    """Page to easily bulk delete all users / blog posts."""

    def get(self):
        self.render("admin.html", True)

    def post(self):
        delete_users, delete_posts = self.getThese(
            "delete_users",
            "delete_posts")

        if delete_users is not None:
            users = SiteUser.all()
            for user in users:
                user.delete()

        if delete_posts is not None:
            posts = BlogPost.all()
            print "Post is", posts
            for one_post in posts:
                one_post.delete()

        self.render("admin.html", True)


# Routing Details
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/welcome', WelcomeHandler),
    ('/img/blogtitle', BlogImage),
    ('/admin', AdminHandler),
    ('/register', RegisterHandler),
    ('/blog', BlogHandler),
    ('/blog/add', NewEntryHandler),
    ('/blog/edit/(.+)', EditEntryHandler),
    ('/blog/react/(.+)', LikePostHandler),
    ('/blog/reactstatus/(.+)', LikePostCheckHandler),
    ('/blog/delete/(.+)', DeleteEntryHandler),
    ('/blog/(.+)', BlogEntryHandler),
    ('/comment_delete/(.+)', DeleteCommentHandler),
    ('/members', MembersHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler)
], debug=True)
