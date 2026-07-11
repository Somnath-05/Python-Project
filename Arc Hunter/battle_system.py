################# battle_system.py - handles game mechanics ############


import random, time, os  # For random numbers, time tracking, terminal commands
from data_manager import load_json
from shop import skill_offers_for
from stats import record_run
import ui  # Shared styling: colors, borders, logo, hp bars

######## Clear terminal using os module
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

######### HP bar display - delegates to the shared, colorized block-style bar
def hp_bar(cur, mx, length=20):
    return ui.hp_bar(cur, mx, length)

####### Calculate damage based on attack and defense values
def damage(att, def_val, crit=False):
    base = max(1, att - def_val//2)  # Base damage reduced by defense
    dmg = int(base * random.uniform(0.8, 1.2))  # Add random variation
    return dmg * 2 if crit else dmg  # Double damage on critical hit

######### Main battle function
def battle_run(player, start_floor=1):
    clear()
    ui.print_banner()
    print()
    print(ui.style("Welcome back to ARC HUNTER!", ui.C.BOLD, ui.C.WHITE))
    print("Your journey continues through the shadows of the arena.")
    print()
    villains = [
        {"name":"Orochimaru","hp":90,"atk":22,"def":12},  # Floor 1 villain
        {"name":"Ultron","hp":110,"atk":28,"def":16},     # Floor 2 villain
        {"name":"Titan Beast","hp":140,"atk":34,"def":18}, # Floor 3 villain
        {"name":"KIRMADA","hp":320,"atk":48,"def":28}     # Floor 4 boss villain
    ]

    floor = start_floor  # Current floor
    damage_total = 0     # Total damage done in this run
    run_start = time.time()  # Run start time for statistics

    # Main game loop for each floor
    while floor <= len(villains) and player['hp'] > 0:
        villain = villains[floor-1].copy()  # Copy current floor villain
        villain['hp'] = int(villain['hp'] * (1 + floor*0.1))  # Scale HP based on floor
        villain['atk'] = int(villain['atk'] * (1 + floor*0.1))  # Scale attack too
        villain['max_hp'] = villain['hp']  # Store max HP for HP bar

        # Special intro for boss fight
        if villain['name'] == "KIRMADA":
            clear()
            print(ui.top())
            print(ui.line_center(ui.style(f"!!! BOSS APPEARS: {villain['name']} !!!", ui.C.BOLD, ui.C.RED)))
            print(ui.bottom())
            time.sleep(1)

        used_skills = set()  # Skills used in this battle

        # Battle loop until villain or player dies
        while villain['hp'] > 0 and player['hp'] > 0:
            # Display battle UI
            box_width = ui.WIDTH
            print(ui.top(box_width))
            title = f"ARC HUNTER  -  Floor {floor} / {len(villains)}"
            print(ui.line_center(ui.style(title, ui.C.BOLD, ui.C.GOLD), box_width))
            print(ui.mid(box_width))
            player_line = (
                f"{ui.style(player['name'], ui.C.BOLD, ui.C.CYAN)}: HP {hp_bar(player['hp'], player['max_hp'], 18)} "
                f"ATK:{player['atk']} DEF:{player['def']} {ui.gold_tag(player['gold'])}"
            )
            print(ui.line(player_line, box_width))
            print(ui.mid(box_width))
            villain_line = f"{ui.style(villain['name'], ui.C.BOLD, ui.C.RED)}: HP {hp_bar(villain['hp'], villain['max_hp'], 30)}"
            print(ui.line(villain_line, box_width))
            print(ui.mid(box_width))
            actions_line = "Actions: [1] Attack   [2] Skill   [3] Defend   [4] Item   [5] Save   [6] Shop"
            print(ui.line(actions_line, box_width))
            print(ui.bottom(box_width))
            print("Choose your next move:")
            cmd = input(ui.style("Enter action number: ", ui.C.CYAN)).strip()

            if cmd == "1":
                # Normal attack
                crit = random.random() < 0.25  # 25% chance of critical hit
                dmg = damage(player['atk'], villain['def'], crit)  # Calculate damage
                villain['hp'] -= dmg  # Reduce villain HP
                damage_total += dmg  # Add to total damage
                crit_tag = ui.style(" - CRITICAL HIT!", ui.C.YELLOW, ui.C.BOLD) if crit else ""
                print(f"You strike {villain['name']} for {dmg} damage" + crit_tag)

            elif cmd == "2":
                # Skill usage
                skills = load_json("skills.json").get(player['key'], [])  # Load player skills
                available = [s for s in skills if s['id'] in player['skills_owned'] and s['id'] not in used_skills]  # Filter available skills

                if not available:
                    print(ui.style("No skills are available yet. Earn new power before using this.", ui.C.GREY))
                    continue

                print(ui.style("Spirit techniques available:", ui.C.CYAN))
                for i,s in enumerate(available, 1):
                    print(f"{i}) {s['name']} - Damage:{s.get('damage',0)} Heal:{s.get('heal',0)}")

                try:
                    choice = int(input("Choose skill number: ")) - 1
                    skill = available[choice]
                    used_skills.add(skill['id'])

                    if skill.get('damage',0) > 0:
                        dmg = damage(skill['damage'] + player['atk']//3, villain['def'])
                        villain['hp'] -= dmg
                        damage_total += dmg
                        print(f"{skill['name']} slams into {villain['name']} for {dmg} damage!")
                    elif skill.get('heal',0) > 0:
                        heal = skill['heal']
                        player['hp'] = min(player['max_hp'], player['hp'] + heal)
                        print(f"{skill['name']} restores {heal} HP!")
                except:
                    print("That selection is not valid.")
                    continue

            elif cmd == "3":
                # Defend action
                print("You raise your guard, hardening your defense for the next strike.")
                player['def'] += 15  # Temporary defense boost
                defended = True  # Set defend flag

            elif cmd == "4":
                # Item usage
                items = load_json("items.json")  # Load items
                print(ui.style("Items:", ui.C.CYAN))  # Show available items
                for i,item in enumerate(items, 1):
                    count = player.get('items', {}).get(item['id'], 0)  # Check item count
                    print(f"{i}) {item['name']} x{count}")

                try:
                    choice = int(input("Choose item number: ")) - 1
                    item = items[choice]
                    if player.get('items', {}).get(item['id'], 0) > 0:
                        if item['effect'] == "heal":
                            player['hp'] = min(player['max_hp'], player['hp'] + item['value'])
                            player['items'][item['id']] -= 1
                            print(f"You use {item['name']} and feel its power surge through you.")
                    else:
                        print("You don't have that item in your pack.")
                except:
                    print("That item selection is not valid.")
                    continue

            elif cmd == "5":
                # Save game
                from save_system import save_game
                save_game({"player": player, "floor": floor, "damage_total": damage_total})  # Save game state
                print(ui.style("Your progress is safely stored.", ui.C.GREEN))
                return  # Save and exit

            elif cmd == "6":
                # Shop access
                from shop import open_shop
                open_shop(player)  # Open shop
                continue
            else:
                print(ui.style("That action is not available.", ui.C.RED))
                continue

            if villain['hp'] <= 0:  # If villain dies
                break

            # Enemy attack phase
            vcrit = random.random() < 0.05  # 5% chance villain critical hit
            vdmg = damage(villain['atk'], player['def'], vcrit)  # Villain damage calculation
            player['hp'] -= vdmg  # Reduce player HP
            vcrit_tag = ui.style(" - CRITICAL HIT!", ui.C.YELLOW, ui.C.BOLD) if vcrit else ""
            print(f"{villain['name']} strikes you for {vdmg} damage" + vcrit_tag)

            # Remove defend effect after each attack
            if 'defended' in locals():
                player['def'] -= 5  # Remove defense boost
                defended = False

        if player['hp'] <= 0:  # If player dies
            print(ui.style("You died!", ui.C.BOLD, ui.C.RED))
            break

        # Floor cleared - victory rewards
        gold_gain = 50 + floor * 40
        player['gold'] += gold_gain
        print(ui.style(f"Victory! You cleared Floor {floor} and earned {gold_gain} gold.", ui.C.BOLD, ui.C.GREEN))

        # Skill shop after each floor
        offers = skill_offers_for(player['key'], 3)
        print("\nA wandering sage appears with new techniques:")
        print("Choose one skill to learn, or press 0 to keep your current path.")
        for i, offer in enumerate(offers, 1):
            print(f"{i}) {offer['name']} - {offer['cost']}g")
        print("0) Continue without new skills")

        try:
            choice = int(input("Which skill do you take? "))
            if 1 <= choice <= len(offers):
                offer = offers[choice-1]
                if player['gold'] >= offer['cost']:
                    player['gold'] -= offer['cost']
                    player['skills_owned'].append(offer['id'])
                    print(f"You learn {offer['name']} and add it to your arsenal.")
                else:
                    print("Your purse is too light for that skill.")
        except:
            print("You continue onward without new skills.")

        player['max_hp'] += 60
        player['hp'] = player['max_hp']
        floor += 1

    # Run complete - record statistics
    run_time = time.time() - run_start  # Calculate total run time
    record_run(player['name'], player['key'], floor-1, player['hp']>0, run_time, player.get('gold',0), damage_total)

    # Final summary
    clear()
    ui.print_banner("QUEST COMPLETE")
    print()
    print("Your final tale is written in the annals of ARC HUNTER:")
    print(f"{ui.style('Floors Cleared:', ui.C.CYAN)} {floor-1}")
    print(f"{ui.style('Damage Dealt:', ui.C.CYAN)} {damage_total}")
    print(f"{ui.style('Gold Collected:', ui.C.CYAN)} {player.get('gold',0)}")
    input(ui.style("Press Enter to return to the main hall...", ui.C.DIM))
