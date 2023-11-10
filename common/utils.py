import json
import os

"""
A helper to load a json from a relative path
"""


def load_json(dirs: list, file: str):
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    target = [parent_dir] + dirs + [file]
    # print("target",target)
    services_file = os.path.join(*target)
    try:
        with open(services_file, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(
            "Could not read json file. It is probably not valid JSON. "
            + str(services_file)
        )
    return data


def string_to_bool(s: str) -> bool:
    # Define a list of string representations of True values
    true_values = ["true", "1", "yes", "on"]

    # Convert the input string to lowercase and check if it's in the list of true values
    return s.lower() in true_values
