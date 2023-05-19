import re


def is_password_incorrect(password):
    return len(password) <= 8 or len(password) >= 50


def is_valid_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(regex, email))
