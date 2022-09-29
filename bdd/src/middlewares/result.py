import sys

sys.path.append("..")
from errors.auth_exception import AuthException

def resultManager(func):
    def inner1(*args, **kwargs):
        try:
            return func(*args, **kwargs), 200
        except Exception as e:
            return str(e), 400
    return inner1