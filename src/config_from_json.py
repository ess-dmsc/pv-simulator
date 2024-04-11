from typing import Dict, List, Tuple


def traverse_json(json_obj, condition_fn, action_fn, path=[]) -> None:
    """
    Recursively traverse the JSON object applying a condition function
    at each node. If the condition is met, applies an action function.

    :param json_obj: The JSON object or part of it being traversed.
    :param condition_fn: A function that takes a node and returns True if the condition is met.
    :param action_fn: A function that performs an action on nodes that meet the condition.
    :param path: The current path to the node, used for tracking the node's location within the JSON.
    """
    if condition_fn(json_obj):
        action_fn(json_obj, path)

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            traverse_json(value, condition_fn, action_fn, path + [key])
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            traverse_json(item, condition_fn, action_fn, path + [index])


def find_modules_with_type(json_obj, module_type, found_modules=[]) -> List[Tuple]:
    """
    Finds all modules within the JSON structure that have the specified type.

    :param json_obj: The JSON object to search within.
    :param module_type: The type of module to find.
    :param found_modules: A list to hold the found modules and their paths.
    :return: A list of tuples with found modules and their paths.
    """

    def condition_fn(node):
        # Checks if the node is a dict, has a 'module' key, and its value matches the module_type
        return (
            isinstance(node, dict)
            and "module" in node
            and node["module"] == module_type
        )

    def action_fn(node, path):
        # Adds the node and its path to the found_modules list
        found_modules.append((node, path))

    # Reset found_modules list to ensure it's empty for each call
    found_modules.clear()
    traverse_json(json_obj, condition_fn, action_fn)
    return found_modules


def find_all_modules(json_obj) -> List[Dict]:
    found_modules = []

    def condition_fn(node):
        # Checks if the node is a dict and has a 'module' key
        return isinstance(node, dict) and "module" in node

    def action_fn(node, path):
        # Checks if 'config' and 'source' exist within the node
        if "config" in node and "source" in node["config"]:
            module_info = {
                "path": "/".join(map(str, path)),  # Convert path to string
                "source": node["config"]["source"],
                "module": node["module"],
            }
            found_modules.append(module_info)

    traverse_json(json_obj, condition_fn, action_fn)
    return found_modules


def traverse_json_named_paths(json_obj, condition_fn, action_fn, path=[]) -> None:
    """
    Recursively traverse the JSON object, only diving deeper into nodes with a "name" key.
    Applies a condition function at each node. If the condition is met, applies an action function.

    :param json_obj: The JSON object or part of it being traversed.
    :param condition_fn: A function that takes a node and returns True if the condition is met.
    :param action_fn: A function that performs an action on nodes that meet the condition.
    :param path: The current path to the node, using names of groups for tracking the node's location.
    """
    if isinstance(json_obj, dict):
        if "name" in json_obj:  # Only add to path if 'name' exists
            current_path = path + [json_obj["name"]]
        else:
            current_path = path

        if condition_fn(json_obj):
            action_fn(json_obj, current_path)

        for key, value in json_obj.items():
            # Only continue traversing if we have not updated the path, or if this is the iteration over children
            if key != "name" and (current_path == path or key == "children"):
                traverse_json_named_paths(value, condition_fn, action_fn, current_path)
    elif isinstance(json_obj, list):
        for item in json_obj:
            traverse_json_named_paths(item, condition_fn, action_fn, path)


def find_all_modules_with_named_paths(json_obj) -> List[Dict]:
    found_modules = []

    def condition_fn(node):
        # Checks if the node is a dict and has a 'module' key
        return isinstance(node, dict) and "module" in node

    def action_fn(node, path):
        # Extract module information if 'config' and 'source' are present
        if "config" in node and "source" in node["config"]:
            module_info = {
                "path": "/".join(path),  # Use the named path
                "config": node["config"],
                "module": node["module"],
            }
            found_modules.append(module_info)

    traverse_json_named_paths(json_obj, condition_fn, action_fn)
    return found_modules


def build_config(json_obj) -> Dict:
    all_modules = find_all_modules_with_named_paths(json_obj)
    config = {}

    for module in all_modules:
        if module["module"] not in ["f144", "tdct"]:
            continue

        if not module["config"]["source"].startswith("SIM_"):
            continue

        config[module["path"]] = {
            "module": module["module"],
            "source": module["config"]["source"]
            if "source" in module["config"]
            else None,
            "topic": module["config"]["topic"] if "topic" in module["config"] else None,
            "dtype": module["config"]["dtype"] if "dtype" in module["config"] else None,
            "value_units": module["config"]["value_units"]
            if "value_units" in module["config"]
            else None,
        }

    return config


if __name__ == "__main__":
    import json

    test_json_path = "/home/jonas/code/nexus-json-templates/odin/odin.json"
    with open(test_json_path, "r") as file:
        json_data = json.load(file)

    config = build_config(json_data)
