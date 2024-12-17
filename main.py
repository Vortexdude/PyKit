import json
import yaml
import os

def _try_as(loader, data, on_error):
    """
    Tries to process the data with the given loader. Returns True if successful, False otherwise.
    """
    try:
        loader(data)
        return True
    except on_error:
        return False

def is_json(data):
    """
    Checks if the given data is valid JSON.
    """
    return _try_as(json.loads, data, json.JSONDecodeError)

def is_yaml(data):
    """
    Checks if the given data is valid YAML.
    """
    return _try_as(yaml.safe_load, data, yaml.YAMLError)

def check_file_type(filepath):
    """
    Checks if the given file is JSON or YAML with proper error handling.
    """
    if not os.path.isfile(filepath):
        return "Error: File not found."

    # Read the file
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        return f"Error: Could not read the file. Details: {e}"

    # Check file type
    if is_json(content):
        return "The file is valid JSON."
    elif is_yaml(content):
        return "The file is valid YAML."
    else:
        return "The file is neither valid JSON nor YAML."

# Example usage
if __name__ == "__main__":
    filepath = "tesst.json"  # Replace with your file path
    result = check_file_type(filepath)
    print(result)