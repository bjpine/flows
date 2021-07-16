def transform():
    print("hello there")

def traverse(obj: dict, path: list=None, callback: callable=None,
             **kwargs) -> dict:
    """Traverse iterable obj, perfroming a deep copy.

    Performs a deep copy of obj recursively, using path to track the current 
    position. Will perform callback on each iteration.

    Args:
        obj (object): An iterable object that will be traversed.
        path (list):  A list consisting of parent key nodes from the 
            current position, and also tuple(s) of position and length 
            when traversing a list.

            For instance::
                path = ["key", (0, 2), "nested_key"]
                obj = {"key":[
                        {"nested_key" : "value"},      <-- at this position
                        {"other_nested_key" : "value"}
                    ]
                }
                (0, 2) = position within list, length of list

            WARNING: This parameter is designed for use by the traverse
            function. Don't use this parameter unless you know what you're
            doing!
        callback (callable): An optional function that is called for each
            each iteration.
            This function takes 3 arguements; path, value (at current pos) and
            kwargs.
        **kwargs:  Any additional attributes to pass to the callback function.
    Returns:
        object: The deep-copy result of obj, or a modified version if applying 
        a callback function.
    """
    if path is None:
        path = []

    if isinstance(obj, dict):
        value = {k: traverse(v, path + [k], callback)
                 for k, v in obj.items()}
    elif isinstance(obj, list): 
        value = [traverse(v, path + [(i, len(obj))], callback)
                 for i, v in enumerate(obj)]
    else:
        value = obj

    # logging.debug("callback={}, path={}, value={}".format(callback, path, value))
    if callback is None:
        return value
    else:
        return callback(path, value, **kwargs)


def to_path(schema: dict, key: object) -> list:
    """Determines the path from the current key based on the provided schema.

    Given the key and schema, determine the "path" as a list representing the
    layers within a nested dict/list object.

    Args:
        schema (dict): A schema dict object
        key (object): Object as key within schema from which to find traversal
            path.
    
    Returns:
        list: A list object representing the path in which we need to traverse.
    """
    target_path = [key]
    if schema[key]["repeating"]:
        target_path.append("[]")
    
    while schema[key]["parent"]:
        parent = [schema[key]["parent"]]
        if schema[schema[key]["parent"]]["repeating"]:
            parent.append("[]")
        
        target_path = parent + target_path
        key = schema[key]["parent"]

    # logging.debug("target_path: {}".format(target_path))
    return target_path


def validate_item(key: object, item: object, schema: dict) -> object:
    """Validates and converts item object.

    Given key and item, perform validation and conversion based on schema.

    Args:
        key (object): The key of item to validate.
        item (object): The object to be validated.
        schema (dict): The schema to validate against.
    
    Returns:
        object: The item, converted based on schema.
    """
    if schema[key]["repeating"]:
        item = [item]
    return item


def add_item(value: object, key: object, item: object) -> object:

    if key in value:
        if isinstance(value[key], list):
            value[key] += item
        else:
            raise "Key {} already in value.".format(key)
    else:
        value[key] = item
        
    return value


def match_path(path: list, target_path: list):
    """Performs match on path and target_path.
    
    Return true/false if path matches target_path. The algorithm will match
    paths based on each item. Special rules apply for items in path that are
    tuples.

    eg: TODO: Add example of paths that match.
    
    Args:
        path (list): A list object representing a path. Items that are tuples
            must match against items in target_path that are "[]", AND the
            reversed int's must not have a difference greater than 1.
            ie: (0, 1).
        target_path (list): A list object representing the target. If items
            within the list are tuples, we assume that the ints will
            'match' also.
    
    Returns:
        bool: True == match
    """
    def match_path_result(path, target_path):
        for i, v in enumerate(path):
            if isinstance(v, tuple):
                if target_path[i] != "[]":
                    return False
                if v[1] - v[0] > 1:
                    return False    
            else:
                if v != target_path[i]:
                    return False
        return True

    result = match_path_result(path, target_path)
    # logging.debug("match_path result={}, path={}, target_path:{}".format(
    #     result, path, target_path
    # ))
    return result


def traverse_add_item(obj: object, schema: dict, key: object,
                      item: object) -> object:
    """Traverse obj and add key/item based on the schema definition.
    
    Determine target_path for key based on schema definition. Refer to 
    target_path function.
    Validate the item and apply any schema masks. Refer to validate_item
    function.
    Traverse obj. Match target_path with path. Refer to match_path
    function. Apply add_item funtion.
    
    Args:
        obj (object): The object that we are traversing and extending.
        schema (dict): The schema that applies to the obj. Used for
            determing our path.
        key (object): The key within the schema we are extending with item.
        item (objecet): The object that we are extending obj with.
    
    Returns:
        object: Will return the modified obj.
    """
    target_path = to_path(schema, key)
    item = validate_item(key, item, schema)

    def transformer(path, value):
        if match_path(path, target_path):
            return add_item(value, key, item)
        else:
            return value

    return traverse(obj, callback=transformer)
