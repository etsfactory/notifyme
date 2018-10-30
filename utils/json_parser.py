import ujson
import ast

def to_json_list(data):
    if isinstance(data, list):
        entry = ujson.dumps([ob.__dict__ for ob in data])
        return ast.literal_eval(entry)
    else: 
        return to_json(data)
        
def to_json(data):
    entry = ujson.dumps(data.__dict__)
    return ast.literal_eval(entry)

def from_json(data):
    return ujson.loads(data)

def dict_keys(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None