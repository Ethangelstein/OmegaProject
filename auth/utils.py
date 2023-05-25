import re
import hashlib


def is_password_incorrect(password):
    return len(password) <= 8 or len(password) >= 50


def is_valid_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(regex, email))


def hash_password(password):
    salt = "NJOXSA?!#"

    salted_password = password.encode("utf-8") + salt.encode("utf-8")

    return hashlib.sha256(salted_password).hexdigest()


def is_valid_password(password, stored_hash):
    hashed_password = hash_password(password)
    return hashed_password == stored_hash
