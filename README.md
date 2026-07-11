# ⚔ ARC HUNTER

A terminal-based text RPG in Python — choose a hero, battle through 4 floors of villains, and climb the Hall of Legends.

> Python Project — Semester 2 · Group 8

---

## About

ARC HUNTER is a fully text-driven dungeon-crawler played entirely in the command line. There's no graphical interface — instead, the game uses colored ANSI text and Unicode box-drawing borders to deliver a polished, game-like feel straight from the terminal.

Pick a hero, fight your way through four escalating floors, learn new skills, gear up at the shop, and see how your runs stack up in the Hall of Legends.

## Features

- **5 playable heroes** — Naruto Uzumaki, Tony Stark (Iron Man), Mikasa Ackerman, Tanjiro Kamado, and Krishh — each with unique HP, Attack, Defense, and Speed stats
- **4-floor campaign** with scaling difficulty, ending in a boss fight against KIRMADA
- **Turn-based combat** — Attack, use Skills, Defend, use Items, Save, or duck into the Shop mid-battle
- **Progression system** — earn gold, learn new skills between floors, and grow your max HP as you advance
- **Persistent stats** — every run (floors reached, wins, gold, damage dealt) is logged to CSV and viewable in the in-game Hall of Legends
- **Save/load support** so you can pick up a run later
- **Styled terminal UI** — colored HP bars, double-line borders, and a logo banner across every screen

## Getting Started

### Requirements
- Python 3.9+
- `pandas` (for stats tracking)

```bash
pip install pandas
```

### Run the game
```bash
cd "Arc Hunter"
python main.py
```

Or from the project root using the helper launcher:
```bash
python run_game.py
```

> **Tip:** Run this in an actual terminal (not a notebook) — the colors and box-drawing borders need a real terminal to render properly.

## Project Structure

```
.
├── run_game.py              # Convenience launcher from the project root
├── Arc Hunter/
│   ├── main.py               # Menu loop and game entry point
│   ├── battle_system.py       # Combat mechanics and battle screen
│   ├── characters.py          # Hero selection
│   ├── shop.py                # Item and skill purchases
│   ├── save_system.py         # Save/load game state
│   ├── data_manager.py        # JSON data loading
│   ├── stats.py                # Run/account tracking via pandas + CSV
│   ├── ui.py                   # Shared styling: colors, borders, HP bars, logo
│   ├── data/                   # Character, item, and skill definitions (JSON)
│   └── tests/                  # Unit tests for core game flow
└── README.md
```

## How to Play

1. Choose your hero from the roster.
2. Battle the villain on each floor — pick an action every turn.
3. Defeat the floor boss to earn gold and unlock a new skill offer.
4. Visit the Shop anytime mid-battle to buy items or skills.
5. Save your progress whenever you need to step away.
6. Clear Floor 4 and defeat KIRMADA to complete the run.

## Tech Stack

Pure Python and the standard library (`os`, `json`, `random`, `time`), plus `pandas` for statistics tracking. No external game engine — the visual layer (colored bars, bordered panels, logo) is built entirely from custom terminal formatting and ANSI escape codes.

## Contributors

Group 8 — Python Project, Semester 2

---

Thanks for playing ARC HUNTER! May your battles be legendary.
