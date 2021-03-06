import src.security as security
import src.dbextensions as dbExtensions


def validate_register(username, password, password2, email):
    """
    Handles validation for registration form. Returns
    a list of any errors encountered while validating.
    """

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

    user = dbExtensions.get_user_from_username(username)
    if user is not None:
        errors.append(
            ("A user with this name already exists. "
                "Please choose another."))

    return errors


def validate_login(username, password):
    """
    Handles validation for login form. Returns
    a list of any errors encountered while validating.
    """

    errors = []

    if len(username) == 0:
        errors.append("Username is required.")

    if len(password) == 0:
        errors.append("Password is required.")

    return errors


def validate_blog_post(title, summary, contents, user_name):
    """
    Handles validation for creating a blog post. Returns
    a list of any errors encountered while validating.
    """

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
    """
    After login form validation is complete, check that the username
    specified matche s auser and that their password is valid.
    """

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
