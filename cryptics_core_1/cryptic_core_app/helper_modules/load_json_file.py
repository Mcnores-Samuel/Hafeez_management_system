#!/usr/bin/env python3
import json

def load_from_json_file(filename):
    """Creates an Object from a JSON file

    args:
        filename: JSON file to create an object from.
    Returns: the object created or Deserialized
    """
    with open(filename) as file:
        obj = json.load(file)
        return (obj)