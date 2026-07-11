# save_system.py -
import json
import os
from pathlib import Path

SAVE_FILE = Path(__file__).resolve().parent / "arc_save.json"


def save_game(state):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    print("Game saved to arc_save.json")


def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("Save file deleted!")
