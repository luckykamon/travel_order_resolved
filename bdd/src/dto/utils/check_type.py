from bson import ObjectId

def checkNone(func):
    def inner1(*args, **kwargs):
        if args[0] is None:
            raise TypeError(f"{func.__name__} : need a field name as first argument")
        if len(args) < 2:
            raise TypeError(f"{func.__name__} : need 2 arguments minimum (field_name, value)")
        
        if args[1] is None:
            if (len(args) == 3) and (args[2] is True):
                raise TypeError(f"{args[0]} : must not be None")
            return None 
        return func(*args, **kwargs)

    return inner1

def check_str_raise(field_name, value, required=True):
    if not isinstance(value, str):
        raise TypeError(f"{field_name} : must be a string")

def check_int_raise(field_name, value, required=True):
    if not isinstance(value, int):
        try:
            value = int(value)
        except:
            raise TypeError(f"{field_name} : must be an integer")

def check_float_raise(field_name, value, required=True):
    if not isinstance(value, float):
        try:
            value = float(value)
        except:
            raise TypeError(f"{field_name} : must be a float")

def check_id_raise(field_name, value, required=True):
    check_str_raise(field_name, value, required=required)
     
    if not ObjectId.is_valid(value):
        raise TypeError(f"{field_name} : must be a valid ObjectId")
  
def check_slug_raise(field_name, value, required=True):
    check_str_raise(field_name, value, required=required)
      
    if " " in value:
        raise TypeError(f"{field_name} : must not contain spaces")
    if "-" in value:
        raise TypeError(f"{field_name} : must not contain dashes")
    if "." in value:
        raise TypeError(f"{field_name} : must not contain dots")
    if not value.islower():
        raise TypeError(f"{field_name} : must be lowercase")
  
def check_zip_code_raise(field_name, value, required=True):
    check_str_raise(field_name, value, required=required)
    
    if (len(value) != 5):
        raise TypeError(f"{field_name} : must be 5 characters long")
    if (not value.isnumeric()):
        raise TypeError(f"{field_name} : must be a number")
    
@checkNone
def check_str(field_name, value, required=True) -> str:
    check_str_raise(field_name, value, required=required)
    return value

@checkNone
def check_int(field_name, value, required=True) -> int:
    check_int_raise(field_name, value, required=required)
    return int(value)

@checkNone
def check_float(field_name, value, required=True) -> float:
    check_float_raise(field_name, value, required=required)
    return float(value)

@checkNone
def check_id(field_name, value, required=True) -> ObjectId:
    check_id_raise(field_name, value, required=required)
    if isinstance(value, ObjectId):
        return value
    return ObjectId(value)

@checkNone
def check_slug(field_name, value, required=True) -> str:
    check_slug_raise(field_name, value, required=required)
    return value

@checkNone
def check_zip_code(field_name, value, required=True) -> str:
    check_zip_code_raise(field_name, value, required=required)
    return value