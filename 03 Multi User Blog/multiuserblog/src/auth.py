import src.security as security
from src.route import Handler
from src.data import SiteUser
from src.validation import (
    validate_register,
    validate_login,
    attempt_user_login)


class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):

        name, password = self.getThese("login-name", "login-password")

        error_messages = validate_login(name, password)

        if len(error_messages) == 0:

            error_messages, result = attempt_user_login(name, password)

            if result:

                # Set current user cookie.
                self.response.headers.add_header(
                    'Set-Cookie',
                    str('user_name=%s' % security.make_cookie_data(
                        name.lower())))

                # Return to main page.
                self.redirect("/")

        self.render(
            "login.html",
            error_messages=error_messages,
            form_user_name=name)


class LogoutHandler(Handler):
    def get(self):

        self.response.delete_cookie('user_name')
        self.redirect("/")


class RegisterHandler(Handler):
    def get(self):

        self.render("register.html", new_id=None)

    def post(self):

        name, pass1, pass2, email = self.getThese(
            "register-name",
            "register-pass1",
            "register-pass2",
            "register-email")

        error_messages = validate_register(name, pass1, pass2, email)

        new_id = None

        if len(error_messages) == 0:
            user = SiteUser(
                username=name.lower(),
                password=security.make_pw_hash(
                    name,
                    pass1,
                    security.make_salt()),
                email=email)
            user.put()
            new_id = user.key()

        self.render(
            "register.html",
            new_id=new_id,
            error_messages=error_messages,
            form_user_name=name,
            form_email=email)
