# shop.py -
from data_manager import load_json
import random
import ui  # Shared styling: colors, borders, logo, hp bars

def skill_offers_for(char_key, n=3):
    skills = load_json("skills.json").get(char_key, [])
    return random.sample(skills, min(n, len(skills)))

def open_shop(player):
    print()
    ui.print_banner("THE MERCHANT'S BAZAAR")
    print(ui.style(f"Your Gold: {player['gold']}", ui.C.GOLD, ui.C.BOLD))
    print(ui.rule())

    items = load_json("items.json")
    print()
    print(ui.style("ITEMS FOR SALE", ui.C.CYAN, ui.C.BOLD))
    print(ui.rule(char="┈"))
    for i, item in enumerate(items, 1):
        print(f"[I{i}] {item['name']} — {item['price']}g")

    skills = load_json("skills.json").get(player['key'], [])
    print()
    print(ui.style("SKILLS AVAILABLE", ui.C.CYAN, ui.C.BOLD))
    print(ui.rule(char="┈"))
    for i, skill in enumerate(skills, 1):
        owned = skill['id'] in player['skills_owned']
        status = ui.style("OWNED", ui.C.GREEN) if owned else f"{skill['cost']}g"
        print(f"[S{i}] {skill['name']} — {status}")

    print()
    print(ui.rule())
    print("Enter the code for your purchase, or type 'exit' to leave the bazaar.")
    print(ui.rule())
    cmd = input(ui.style("Command: ", ui.C.CYAN)).lower()

    if cmd == "exit":
        print("You leave the bazaar and continue your quest.")
        return

    if cmd.startswith("i"):
        try:
            idx = int(cmd[1:]) - 1
            item = items[idx]
            if player['gold'] >= item['price']:
                player['gold'] -= item['price']
                player['items'][item['id']] = player['items'].get(item['id'], 0) + 1
                print(ui.style(f"You purchase {item['name']} and add it to your pack.", ui.C.GREEN))
            else:
                print(ui.style("Your purse is too light for that item.", ui.C.RED))
        except:
            print(ui.style("That shop code is not valid.", ui.C.RED))

    elif cmd.startswith("s"):
        try:
            idx = int(cmd[1:]) - 1
            skill = skills[idx]
            if skill['id'] in player['skills_owned']:
                print("You already know that skill.")
            elif player['gold'] >= skill['cost']:
                player['gold'] -= skill['cost']
                player['skills_owned'].append(skill['id'])
                print(ui.style(f"You acquire the skill {skill['name']}.", ui.C.GREEN))
            else:
                print(ui.style("Your purse is too light for that skill.", ui.C.RED))
        except:
            print(ui.style("That skill code is not valid.", ui.C.RED))
