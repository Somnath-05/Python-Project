# characters.py - Handles character selection
from data_manager import load_json  # For loading JSON files
import ui  # Shared styling: colors, borders, logo, hp bars

def choose_character():
    """Let player select character and return character data"""
    chars = load_json("characters.json")
    ui.print_banner("CHOOSE YOUR HERO")
    print()
    print("Each hero carries a unique legacy and special power. Choose wisely.")
    print()
    for i, c in enumerate(chars, 1):
        print(f"{ui.style(f'[{i}]', ui.C.GOLD, ui.C.BOLD)} {ui.style(c['name'], ui.C.BOLD)}")
        print(f"    {c['short']}")
        print(f"    HP: {c['hp']}   ATK: {c['atk']}   DEF: {c['def']}   SPD: {c['spd']}")
        print()
    print(ui.rule())

    while True:
        try:
            choice = int(input("Enter the number of your chosen hero: "))
            if 1 <= choice <= len(chars):
                char = chars[choice - 1].copy()
                char['gold'] = 50
                char['skills_owned'] = []
                char['items'] = {}
                print(ui.style(f"{char['name']} joins your party!", ui.C.GREEN, ui.C.BOLD))
                input(ui.style("Press Enter to step into the arena...", ui.C.DIM))
                return char
        except:
            pass
        print(ui.style("That choice doesn't exist. Try again.", ui.C.RED))
