import json

class Reader:
    def __init__(self, path):
        with open(path, "r") as f:
            self.data = json.load(f)

