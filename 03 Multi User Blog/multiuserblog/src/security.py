import hmac
import string
import hashlib
import random


# Should be stored in another location (so it is not shared)
SECRET = 'imsosecret'


def valid_pw(name, pw, hash):
    salt = hash.split(",")[1]
    return hash == make_pw_hash(name, pw, salt)


def make_pw_hash(name, pw, salt):
    hash = hashlib.sha256(name.lower() + pw + salt).hexdigest()
    return "%s,%s" % (hash, salt)


def make_salt():
    return ''.join(random.choice(string.letters) for _ in range(5))


def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


def make_cookie_data(value):
    return "%s|%s" % (value, hash_str(value))


def cookie_is_valid(cookie):
    if cookie is not None:
        value = cookie.split("|")[0]
        if cookie == make_cookie_data(value):
            return value
    else:
        return None

def cookie_value(cookie):
    return cookie if cookie is None else cookie.split("|")[0]

def is_logged_in(request):
    return cookie_value(request.cookies.get('user_name', None)) is not None
