from bson import ObjectId

def checkNotNone(func):
    def inner1(*args, **kwargs):
        if args[0] is None:
            raise TypeError(f"{func.__name__} : need a field name as first argument")
        if len(args) != 2:
            raise TypeError(f"{func.__name__} : need 2 arguments")
        
        if args[1] is None:
            return None 
        return func(*args, **kwargs)    
    return inner1

@checkNotNone
def check_str(field_name, value):
    if not isinstance(value, str):
        raise TypeError(f"{field_name} : must be a string")
    return value
    
@checkNotNone
def check_int(field_name, value):
    if not isinstance(value, int):
        try:
            value = int(value)
        except:
            raise TypeError(f"{field_name} : must be an integer")

    return value

@checkNotNone
def check_float(field_name, value):
    if not isinstance(value, float):
        try:
            value = float(value)
        except:
            raise TypeError(f"{field_name} : must be a float")
        
    return value

@checkNotNone
def check_id(field_name, value):
    check_str(field_name, value)
    
    if not ObjectId.is_valid(value):
        raise TypeError(f"{field_name} : must be a valid ObjectId")
    
    return value
  
@checkNotNone  
def check_slug(field_name, value):
    check_str(field_name, value)
    
    if " " in value:
        raise TypeError(f"{field_name} : must not contain spaces")
    if "-" in value:
        raise TypeError(f"{field_name} : must not contain dashes")
    if "." in value:
        raise TypeError(f"{field_name} : must not contain dots")
    if not value.islower():
        raise TypeError(f"{field_name} : must be lowercase")
    
    return value
 
@checkNotNone   
def check_zip_code(field_name, value):
    check_str(field_name, value)
    
    if (len(value) != 5):
        raise TypeError(f"{field_name} : must be 5 characters long")
    if (not value.isnumeric()):
        raise TypeError(f"{field_name} : must be a number")
    
    return value