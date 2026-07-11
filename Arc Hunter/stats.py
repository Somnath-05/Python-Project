# stats.py - Statistics tracking system
import time
from pathlib import Path

import pandas as pd  # For data analysis

BASE_DIR = Path(__file__).resolve().parent
ACCOUNTS_FILE = BASE_DIR / "accounts.csv"  # Player accounts file name
RUNS_FILE = BASE_DIR / "runs.csv"  # Game runs file name


def ensure():
    """Create statistics files if they don't exist"""
    try:
        pd.read_csv(ACCOUNTS_FILE)  # Try to read accounts file
    except Exception:
        df = pd.DataFrame(columns=["player_name", "char_key", "best_floor", "runs", "wins", "gold_total"])
        df.to_csv(ACCOUNTS_FILE, index=False)  # Create empty CSV file

    try:
        pd.read_csv(RUNS_FILE)  # Try to read runs file
    except Exception:
        df = pd.DataFrame(columns=["player_name", "date", "floor_reached", "won", "time_sec", "gold_earned", "damage_done"])
        df.to_csv(RUNS_FILE, index=False)  # Create empty CSV file


def record_run(player_name, char_key, floor_reached, won, time_sec, gold_earned, damage_done):
    """Record game run data and update statistics."""
    ensure()  # Ensure files exist

    df = pd.read_csv(RUNS_FILE)  # Load runs file
    new_row = pd.DataFrame({
        "player_name": [player_name],
        "date": [time.strftime("%Y-%m-%d %H:%M:%S")],
        "floor_reached": [floor_reached],
        "won": [int(bool(won))],
        "time_sec": [int(time_sec)],
        "gold_earned": [int(gold_earned)],
        "damage_done": [int(damage_done)],
    })
    df = pd.concat([df, new_row], ignore_index=True)  # Add new row
    df.to_csv(RUNS_FILE, index=False)  # Save updated data

    ac = pd.read_csv(ACCOUNTS_FILE)  # Load accounts file
    if player_name in ac["player_name"].values:
        idx = ac.index[ac["player_name"] == player_name][0]
        ac.at[idx, "runs"] = ac.at[idx, "runs"] + 1
        ac.at[idx, "wins"] = ac.at[idx, "wins"] + int(bool(won))
        ac.at[idx, "gold_total"] = ac.at[idx, "gold_total"] + gold_earned
        if floor_reached > ac.at[idx, "best_floor"]:
            ac.at[idx, "best_floor"] = floor_reached
    else:
        new_account = pd.DataFrame({
            "player_name": [player_name],
            "char_key": [char_key],
            "best_floor": [floor_reached],
            "runs": [1],
            "wins": [int(bool(won))],
            "gold_total": [gold_earned],
        })
        ac = pd.concat([ac, new_account], ignore_index=True)
    ac.to_csv(ACCOUNTS_FILE, index=False)  # Save updated accounts
