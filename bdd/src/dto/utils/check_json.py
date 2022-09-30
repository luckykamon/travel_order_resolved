
def check_json(json):
    if json is None:
        raise ValueError("No JSON found")
        
def exist_in_json(json, key):
    return key not in json.keys()

def get_key(json, key):
    if exist_in_json(json, key):
        return None
    return json[key]
    
    