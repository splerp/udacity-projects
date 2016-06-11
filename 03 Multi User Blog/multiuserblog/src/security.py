import hmac

def hash_str(s):
    return hmac.new(secret, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    value = h.split("|")[0]
    return value if make_secure_val(value) == h else None

def make_salt():
    return ''.join(random.choice(string.letters) for _ in range(5))