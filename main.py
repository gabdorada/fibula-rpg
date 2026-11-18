import random
from models import Player, Monster, Item
from database import Database

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

# 2. Function to display game over
def game_over():
    print('The game is over.')
    print('Thanks for playing!')
    exit(1)

# 3. Generic Combat Function (uses methods from the Character class)
def handle_combat(attacker, defender):
    damage = attacker.attack(defender)
    if not defender.is_alive:
        print(f'{defender.name} died!')
        return False
    return True

# 4. Main Game Function
def main():
    show_title()
    db = Database()

    # Game Load or New Game Choice
    choice = input('1. New Game\n2. Load Game\n')

    player = None 
    if choice == 2:
        hero_name = input('Enter your saved heroine/hero name: ')
        player = db.load_player(hero_name)
        if not player:
            print('Character not found! Creating a new game...')
            
    if not player:
        hero_name = input('Enter the name of your heroine/hero: ')
        player = Player(name=hero_name, hp=100, max_exp=100, strength=3)

    # Save initial state to database
    db.save_player(player)
    print('\n')

    current_monster = None

    while True:
        # If there is no active monster, generate a new one based on the player's level
        if current_monster is None or not current_monster.is_alive:
            current_monster = Monster.spawn_for_level(player.level)
            print(f'\nA wild {current_monster.name} appears!')
            print(f'HP: {current_monster.hp}\n')

        # Quick Status Panel
        print(f'{player.name}: {player.hp}\100')
        print(f'Level: {player.level}')
        print('What do you want to do?')
        print('1. Attack')
        print('2. Use item')
        print('3. Run away')
        print('4. View status')
        print('5. Quite game')

        try:
            option = int(input('> '))
        except ValueError:
            print('Invalid option!\n')
            continue

        print('\n')

        if option == 1:
            # Player's Turn
            print(f'{player.name} attacks {current_monster.name}!')
            monster_survived = handle_combat(player, current_monster)

            if monster_survived:
                # Monster's Turn (Counterattack)
                print(f'{current_monster.name} counter-attacks {player.name}!')
                player_survived = handle_combat(current_monster, player)
                if not player_survived:
                    game_over()
                else:
                    # Monster defeated: EXP reward
                    print(f'You gained {current_monster.exp_reward} XP!')
                    leveled_up = player.gain_exp(current_monster.exp_reward)
                    if leveled_up:
                        print(f'Level Up! You are now level {player.level}!')

                    # Chance to drop a potion (Item)
                    if random.random() <= 0.5: # 50% chance of loot
                        potion = Item(name='Potion', item_type='potion', effect_value=20)
                        player.add_item(potion)
                        print('You got a potion!')

                    current_monster = None # Need to generate a new monster in the next round

        elif option == 2:
            # Use item from inventory
            if not player.inventory:
                print('Your inventory is empty.\n')
            else:
                print('Inventory:')
                for index, item in enumerate(player.inventory):
                    print(f'{index + 1}. {item.name} (+{item.effect_value} HP)')

                item_potion = int(input('Choose an item (or 0 to cancel): '))
                if item_potion > 0:
                    success = print(f'You used a potion. Your HP is now {player.hp}\n')
                else:
                    print(f'Invalid item choice.\n')

        elif option == 3:
            # Attempt to escape (50% chance)
            success = random.choice([True, False])
            if success:
                print(f'{player.name} escaped successfully!\n')
                current_monster = None # Resets the current monster
            else:
                print(f'{player.name} could not escape.\n')
                # Monster attacks if escape fails
                player_survived = handle_combat(current_monster, player)
                if not player_survived:
                    game_over()

        elif option == 4:
            # View detailed status
            print(f'=== {player.name} Status ===')
            print(f'HP: {player.hp}')
            print(f'LV: {player.level}')
            print(f'EXP: {player.exp} / {player.required_exp}')
            print(f'{player.required_exp - player.exp} XP to level up')
            print(f'Strength: {player.strength}')
            print(f'Inventory item: {len(player.inventory)}\n')

        elif option == 5:
            game_over()
        else:
            print('Invalid option!\n')

if __name__ == "__main__":
    main()