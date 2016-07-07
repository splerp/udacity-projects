import hmac
import string
import hashlib
import random

# use bcrypt, not sha256.

def valid_pw(name, pw, hash):
    salt = hash.split(",")[1]
    return hash == make_pw_hash(name, pw, salt)

def make_pw_hash(name, pw, salt):
    hash = hashlib.sha256(name.lower() + pw + salt).hexdigest()
    return "%s,%s" % (hash, salt)

def make_salt():
    return ''.join(random.choice(string.letters) for _ in range(5))

SECRET = 'imsosecret' # Make it a long string of random chars stored in another location (so it is not shared)
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_cookie_value(value):
    return "%s|%s" % (value, hash_str(value))
    
def cookie_is_valid(cookie_value):
    actual_data = cookie_value.split("|")[0]
    if cookie_value == make_cookie_value(actual_data):
        return actual_data