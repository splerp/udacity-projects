import src.security as security
import src.dbextensions as dbExtensions


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
