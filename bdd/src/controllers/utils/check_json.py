
def check_json(json):
    if json is None:
        raise ValueError("No JSON found")

def exist_or_raise(json, key):
    if key not in json.keys():
        raise ValueError("Missing fields")
    return json[key]
        
def exist_or_none(json, key):
    if key not in json.keys():
        return None
    return json[key]