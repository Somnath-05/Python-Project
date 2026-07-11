# main.py - Main game file
import os  # For screen clearing
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")

from characters import choose_character  # Character selection
from battle_system import battle_run  # Battle system
from save_system import load_game, delete_save  # Save/load system
from stats import ACCOUNTS_FILE, RUNS_FILE, ensure  # Statistics tracking
import ui  # Shared styling: colors, borders, logo, hp bars


def clear():
    # Clear screen for Windows and Linux
    os.system('cls' if os.name == 'nt' else 'clear')


def intro():
    """Game introduction screen - shows logo and description"""
    clear()
    print(ui.top())
    ui.print_logo()
    print(ui.mid())
    print(ui.style("Welcome to ARC HUNTER!", ui.C.BOLD, ui.C.WHITE))
    print("A world where heroes rise through the ruins, wielding power and courage to face legendary foes.")
    print("""You will choose your champion, battle fearsome villains, gather treasure, and learn mighty skills.
Only the strongest survive each floor. Will your name be etched in the Hall of Legends?""")
    print(ui.bottom())
    print()
    input(ui.style("Press Enter to step into the arena...", ui.C.DIM))


def show_stats():
    """Display player statistics - reads data from CSV files using pandas"""
    clear()
    ui.print_banner("HALL OF LEGENDS")
    print()

    try:
        import pandas as pd
        if ACCOUNTS_FILE.exists():
            df = pd.read_csv(ACCOUNTS_FILE)
            if not df.empty:
                print(ui.style("HEROES IN HISTORY", ui.C.BOLD, ui.C.GOLD))
                print(ui.rule())
                # Print player data
                for _, row in df.iterrows():
                    print(f"{ui.style('Player:', ui.C.CYAN)} {row['player_name']}")
                    print(f"{ui.style('Character:', ui.C.CYAN)} {row['char_key']}")
                    print(f"{ui.style('Best Floor:', ui.C.CYAN)} {row['best_floor']}")
                    print(f"{ui.style('Total Runs:', ui.C.CYAN)} {row['runs']}")
                    print(f"{ui.style('Wins:', ui.C.CYAN)} {row['wins']}")
                    print(f"{ui.style('Total Gold:', ui.C.CYAN)} {row['gold_total']}")
                    print(ui.rule())
            else:
                print("The Hall of Legends is still empty. No heroes recorded yet.")
        else:
            print("The Hall of Legends is still empty. No heroes recorded yet.")

        # Check runs file
        if RUNS_FILE.exists():
            df_runs = pd.read_csv(RUNS_FILE)
            if not df_runs.empty:
                print()
                print(ui.style("RECENT RUNS", ui.C.BOLD, ui.C.GOLD))
                print(ui.rule())
                recent_runs = df_runs.tail(5)  # Last 5 runs
                for _, run in recent_runs.iterrows():
                    status = ui.style("WON", ui.C.GREEN) if run['won'] else ui.style("LOST", ui.C.RED)
                    print(f"{run['player_name']} - Floor {run['floor_reached']} - {status}")
                    print(f"  Time: {run['time_sec']}s | Gold: {run['gold_earned']} | Damage: {run['damage_done']}")
                    print(ui.rule())
            else:
                print("\nNo recent quests have been chronicled yet.")
        else:
            print("\nNo recent quests have been chronicled yet.")

    except Exception as e:
        print(f"Error loading statistics: {e}")

    print()
    input(ui.style("Press Enter to return to the main hall...", ui.C.DIM))


def main():
    """Main function - game main loop"""
    ensure()  # Create statistics files if they don't exist
    intro()  # Show introduction screen

    while True:  # Main game loop
        clear()
        ui.print_banner("MAIN MENU")
        print()
        print(f"  {ui.style('1)', ui.C.GOLD)} Begin New Quest")
        print(f"  {ui.style('2)', ui.C.GOLD)} Continue Saved Journey")
        print(f"  {ui.style('3)', ui.C.GOLD)} Abandon Saved Adventure")
        print(f"  {ui.style('4)', ui.C.GOLD)} View the Hall of Legends")
        print(f"  {ui.style('5)', ui.C.GOLD)} Retreat from the battlefield")
        print()
        print(ui.rule())

        choice = input(ui.style("Select your path: ", ui.C.CYAN)).strip()

        if choice == "1":
            # Start new game
            player = choose_character()  # Select character
            player['max_hp'] = player['hp']  # Set max HP
            player['gold'] = 50  # Starting gold
            player['skills_owned'] = []  # Empty skills list
            player['items'] = {}  # Empty items dictionary
            battle_run(player, 1)  # Start battle on floor 1
        elif choice == "2":
            # Load saved game
            state = load_game()
            if state:
                battle_run(state['player'], state.get('floor', 1))
            else:
                print("No saved adventure was found.")
                input(ui.style("Press Enter to return to the main hall...", ui.C.DIM))
        elif choice == "3":
            # Delete save file
            if input("Are you sure you want to abandon your save? (y/n): ").lower() == "y":
                delete_save()
                print("Your save has been discarded.")
                input(ui.style("Press Enter to return to the main hall...", ui.C.DIM))
        elif choice == "4":
            # Show statistics
            show_stats()
        elif choice == "5":
            # Exit game
            print(ui.style("Thanks for playing ARC HUNTER!", ui.C.BOLD, ui.C.GOLD))
            print("May your battles be legendary!")
            break
        else:
            print(ui.style("That path is blocked. Choose again.", ui.C.RED))
            input(ui.style("Press Enter to continue your journey...", ui.C.DIM))


if __name__ == "__main__":
    main()  # Start program
