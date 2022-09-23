import os
import sys

sys.path.append("..")
from errors.auth_exception import AuthException

def auth_token(token):
    if os.getenv("API_TOKEN") is None:
        raise Exception("API_TOKEN env variable is not set")
    if token is None:
        raise AuthException("Missing token")
    if token != os.getenv("API_TOKEN"):
        raise AuthException("Invalid token")
