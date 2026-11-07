import random


# 1. Function to display the opening title
def show_title():
    title = r""" 
                \||/
                |  @___oo
      /\  /\   / (__,,,,|
     ) /^\) ^\/ _)
     )   /^\/   _)
     )   _ /  / _)
 /\  )/\/ ||  | )_)
<  >      |(,,) )__)
 ||      /    \)___)\
 | \____(      )___) )___
  \______(_______;;; __;;; 
"""
    print(title)
    print('Welcome to FIBULA RPG!')


# 2. Function to start a new game
def start_game():
    name = input('Enter the name of your heroine/hero: ')
    hp = 100
    level = 1
    strength = 3
    exp = 0
    inventory = []  # An empty list (a backpack with no items for now)
    is_alive = True  # True means that the character is alive

    return name, hp, level, strength, exp, inventory, is_alive


# 3. Function to draw a monster
def draw_monster(player_level):
    # Monster list: [name, hp, strength, exp]
    slime = ['slime', 10, 2, 10]
    goblin = ['goblin', 20, 4, 20]
    troll = ['troll', 40, 8, 40]
    orc = ['orc', 80, 16, 80]
    mummy = ['mummy', 160, 32, 160]
    chimera = ['chimera', 320, 64, 320]
    dragon = ['dragon', 1000, 100, 1000]

    if player_level < 5:
        return random.choice([slime, goblin, troll])
    elif player_level < 10:
        return random.choice([orc, mummy, chimera])
    else:
        return dragon


# 4. Function to display game over
def game_over():
    print('The game is over.')
    print('Thanks for playing!')
    exit(1)


# 5. Function for the player's or enemy's attack
def attack(attacker_name, attacker_strength, defender_name, defender_hp, defender_strength):
    attacker_luck = random.randint(0, 6)
    defender_luck = random.randint(0, 6)

    if attacker_luck == 6:
        print(f'{attacker_name} landed a critical hit!')
    elif attacker_luck > 0:
        print(f'{attacker_name} landed an attack!')
    else:
        print(f'{attacker_name} missed the strike!')

    damage = attacker_strength * attacker_luck - defender_strength * defender_luck

    if damage > 0:
        print(f'{defender_name} took {damage} damage!')
        defender_hp = defender_hp - damage
    else:
        print(f'{defender_name} took no damage!')

    if defender_hp <= 0:
        print(f'{defender_name} died!')
        return 0, False  # Defender died
    else:
        return defender_hp, True  # Defender is alive


# 6. Function to calculate level up
def calculate_level(player_level, player_exp, player_hp, player_strength, monster_exp):
    player_exp = player_exp + monster_exp
    required_exp = 3 ** player_level

    if player_exp >= required_exp:  # Check if exp is enough to level up
        print('Level Up!')
        player_level += 1
        player_hp = 100
        player_strength = player_strength * 2

    return player_level, player_exp, player_hp, player_strength


# 7. Function to get a potion
def get_potion():
    chance = random.random()
    if chance <= 2.0:
        print('You got a potion!')
        return 'Potion'
    else:
        return None


# 8. Function to use an item
def use_item(player_inventory, player_hp):
    if not player_inventory:  # Empty inventory
        print('Your inventory is empty.\n')
    else:
        print('Inventory:')
        for index, item in enumerate(player_inventory):
            print(f'{index + 1}. {item}')
        item_option = int(input('Choose an item (or 0 to cancel): '))
        if item_option == 0:
            print('\n')
        else:
            chosen_item = player_inventory[item_option - 1]
            if chosen_item == 'Potion':
                print('You used a potion.')
                player_hp += 20
                if player_hp > 100:
                    player_hp = 100
                print(f'Your HP is now {player_hp}\n')
                player_inventory.pop(item_option - 1)
            else:
                print('Invalid item.\n')

    return player_hp, player_inventory


# 9. Function to run away
def run_away(player_name):
    success = random.choice([True, False])
    if success:
        print(f'{player_name} escaped successfully!\n')
        return True  # Escaped
    else:
        print(f'{player_name} could not escape.\n')
        return False  # Failed to escape


# 10. Main game function
def main():
    show_title()
    (player_name, player_hp, player_level, player_strength,
     player_exp, player_inventory, player_alive) = start_game()
    print('\n')

    fighting_monster = False

    while True:
        if not fighting_monster:
            monster_name, monster_hp, monster_strength, monster_exp = draw_monster(player_level)

            print(f'\nA wild {monster_name} appears!')
            print(f'HP: {monster_hp}\n')
            fighting_monster = True
            monster_alive = True
        else:
            print(f'\nYou are fighting a {monster_name}!')
            print(f'HP: {monster_hp}\n')

        print(f'{player_name}: {player_hp}/100')
        print(f'Level: {player_level}')
        print('What do you want to do?')
        print('1. Attack')
        print('2. Use item')
        print('3. Run away')
        print('4. View status')
        print('5. Quit game')
        option = int(input('> '))

        if option == 1:
            print('\n')
            # Player attacks monster
            monster_hp, monster_alive = attack(player_name, player_strength, monster_name, monster_hp, monster_strength)
            print('\n')
            if monster_alive:
                # Monster attacks player
                player_hp, player_alive = attack(monster_name, monster_strength, player_name, player_hp, player_strength)
                print('\n')
                if not player_alive:
                    game_over()
            else:
                # Player gains experience
                print(f'You gained {monster_exp} XP!')
                player_level, player_exp, player_hp, player_strength = calculate_level(
                    player_level, player_exp, player_hp, player_strength, monster_exp
                )
                # Might get an item
                potion = get_potion()
                if potion is not None:
                    player_inventory.append(potion)
                fighting_monster = False
                continue
        elif option == 2:
            player_hp, player_inventory = use_item(player_inventory, player_hp)
            continue
        elif option == 3:
            escaped = run_away(player_name)
            if escaped:
                fighting_monster = False
                continue
            else:
                # Monster attacks player
                player_hp, player_alive = attack(monster_name, monster_strength, player_name, player_hp, player_strength)
                print('\n')
                if not player_alive:
                    game_over()
        elif option == 4:
            print(f'\n{player_name}')
            print(f'HP: {player_hp}')
            print(f'LV: {player_level}')
            print(f'EXP: {player_exp}')
            next_level_exp = 3 ** player_level
            print(f'{next_level_exp - player_exp} XP to level up')
            print(f'Strength: {player_strength}')
            print(f'Inventory: {player_inventory}\n')
            continue
        elif option == 5:
            game_over()
        else:
            print('Invalid option!\n')
            continue


if __name__ == "__main__":
    main()