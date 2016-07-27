from google.appengine.ext import db


class SiteUser(db.Model):
    """A DB Entity"""
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    description = db.TextProperty()
    joindate = db.DateTimeProperty(auto_now_add=True)


class BlogPost(db.Model):
    """A DB Entity"""
    title = db.StringProperty(required=True)
    contents = db.TextProperty(required=True)
    summary = db.StringProperty()
    date_posted = db.DateTimeProperty(auto_now_add=True)

    title_image = db.BlobProperty()

    owner = db.ReferenceProperty(SiteUser,
                                 required=True,
                                 collection_name='blog_posts')


class BlogPostReaction(db.Model):

    blog_post = db.ReferenceProperty(BlogPost,
                                     required=True,
                                     collection_name='reactions')

    site_user = db.ReferenceProperty(SiteUser,
                                     required=True,
                                     collection_name='reactions')

    reaction_type = db.StringProperty(required=True,
                                      choices=('like', 'dislike'))

    date_liked = db.DateTimeProperty(auto_now_add=True)
