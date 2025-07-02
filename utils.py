import json

def load(json_file):
    with open(json_file) as f:
        data = json.load(f)
        return data