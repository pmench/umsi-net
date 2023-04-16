import json
import pprint


def print_pretty(obj):
    """
    TODO: Write docstring
    :param obj:
    :return:
    """
    pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=100)
    return pp.pprint(obj)


def read_json(filepath, encoding='utf-8'):
    """
    Deserializes JSON object and returns a list or dictionary.

    :param filepath: (str) name of path for file.
    :param encoding: (str) name of encoding for file.
    :return: dict | list representation of JSON object.
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)


def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """
    Serializes an object as JSON.

    :param filepath: (str) name of path for file
    :param data: (dict | list) the data to be encoded as JSON and written to file.
    :param encoding: (str) name of the encoding for file.
    :param ensure_ascii: (bool) whether non-ASCII characters are printed as-is. If True, non-ASCII characters
        are escaped.
    :param indent: the number of "pretty printed" indentation spaces to apply to encoded JSON.
    :return: None.
    """
    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)


def update_cache(filepath, data, key=None):
    """
    Updates an existing cache file with new data. If a key is passed, it attempts to append the data to the key's value.

    :param filepath: (str) path to cache.
    :param data: (list | dict) data to add to cache.
    :param key: key update or add to cache
    :return: None.
    """
    cached = read_json(filepath)
    try:
        if key:
            if key in cached.keys():
                if isinstance(data, dict):
                    cached[key].update(data)
                elif isinstance(data, list):
                    cached[key].extend(data)
            else:
                cached[key] = data
        else:
            cached.update(data)
    except AttributeError as e:
        print(f"Cannot update value: {e}")
    write_json(filepath, cached)


def save_cache(filepath, data, key=None):
    """
    Writes data to given filepath in JSON format to create a cache. If a key is provided, it adds
    the given data as values to the key.

    :param filepath:
    :param data:
    :param key:
    :return:
    """
    cache = {}
    if key:
        cache[key] = data
        write_json(filepath, cache)
        return cache
    else:
        write_json(filepath, data)
