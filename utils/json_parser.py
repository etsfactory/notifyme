import ujson
import ast

def to_json_list(data):
    entry = ujson.dumps([data.__dict__])
    return ast.literal_eval(entry)

def to_json(data):
    entry = ujson.dumps(data.__dict__)
    return ast.literal_eval(entry)

def from_json(data):
    return ujson.loads(data)