# data_manager.py - JSON data loader
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(name):
    path = os.path.join(BASE_DIR, "data", name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
