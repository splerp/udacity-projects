#Integer, Float, String, Date, Time, DateTime, Email, Link, PostalAddress

from google.appengine.ext import db

# A DB entity
class SiteUser(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()
    description = db.TextProperty()
    joindate = db.DateTimeProperty(auto_now_add = True)

# A DB entity
class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    contents = db.TextProperty(required = True)
    summary = db.StringProperty() 
    date_posted = db.DateTimeProperty(auto_now_add = True)
    
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
                                      
    date_liked = db.DateTimeProperty(auto_now_add = True)



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