
def __check_json(json):
    if json is None:
        raise ValueError("No JSON found")
        
def exist_in_json_or_raise(json, key):
    __check_json(json)
    
    if key not in json.keys():
        raise ValueError("Missing fields")
    return json[key]