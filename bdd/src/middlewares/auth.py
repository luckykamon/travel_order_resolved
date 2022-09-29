import os
import sys
from flask import request

sys.path.append("..")
from errors.auth_exception import AuthException

def __auth_token(token):
    if token is None:
        raise AuthException("Missing token")
    if token != os.getenv("API_TOKEN"):
        raise AuthException("Invalid token")

def isAuth(func):
    def inner1(*args, **kwargs):
        try:
            __auth_token(request.headers.get('api_key'))
            return func(*args, **kwargs)
        except AuthException as e:
            return str(e), 401
    return inner1