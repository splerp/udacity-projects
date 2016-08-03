from google.appengine.ext import db


def get_user_from_username(username):
    query = db.GqlQuery(
        ("SELECT * FROM SiteUser"
         "WHERE username = '%s'") % username.lower())

    # Retrieves first valid row, or None
    return query.get()
