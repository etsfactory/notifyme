import ujson
import ast


def to_json_list(data):
    if isinstance(data, list):
        if data:
            if (not isinstance(data[0], dict)):
                entry = ujson.dumps([ob.__dict__ for ob in data])
                return ast.literal_eval(entry)
            else:
                return data
        else:
            return []
    if data:
        entry = ujson.dumps([ob for ob in data])
        return ast.literal_eval(entry)
    else:
        return []


def to_json(data):
    return ujson.dumps(data)


def from_json(data):
    return ujson.loads(data)


def dict_keys(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None
