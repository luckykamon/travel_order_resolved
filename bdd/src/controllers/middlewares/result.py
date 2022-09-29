from enum import Enum
import os
import sys
from flask import jsonify

sys.path.append("..")
from errors.auth_exception import AuthException

class TypeResult(Enum):
    JSON = "json"
    TEXT = "text"

# def annotation for the decorator with parameter
def resultManager(type = TypeResult.TEXT):    
    if (not isinstance(type, TypeResult)):
        raise ValueError("type must be a TypeResult")
    
    def inner1(func):
        def inner2(*args, **kwargs):
            try:
                if(type == TypeResult.JSON):
                    return jsonify(func(*args, **kwargs)), 200
                else:
                    return str(func(*args, **kwargs)), 200
            except Exception as e:
                return str(e), 400
        return inner2
    return inner1