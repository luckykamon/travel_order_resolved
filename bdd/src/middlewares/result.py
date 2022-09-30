from enum import Enum
from flask import jsonify

class ResultManagerType(Enum):
    JSON = "json"
    TEXT = "text"

def resultManager(type: ResultManagerType):
    if not isinstance(type, ResultManagerType):
        raise ValueError("The type must be a ResultManagerType")
    
    def resultManagerInner1(func):
        def resultManagerInner2(*args, **kwargs):
            try:
                if type == ResultManagerType.JSON:
                    return jsonify(func(*args, **kwargs)), 200
                else:
                    return str(func(*args, **kwargs)), 200
            except Exception as e:
                #raise e
                return str(e), 400
        # Renaming the function name:
        resultManagerInner2.__name__ = func.__name__
        return resultManagerInner2        
    return resultManagerInner1