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
    force = 3
    exp = 0
    inventory = [] # An empty list (a backpack with no items for now)
    live_status = True # True means that the character is alive

    return name, hp, level, force, exp, inventory, live_status

# 3. Function to draw a monster
def draw_monster(player_level):
    # Monster list: [name, hp, strength, exp]
    slime = ['slime', 10, 2, 10]
    goblin = ['goblin', 20, 4, 20]
    troll = ['troll', 40, 8, 40]
    orc = ['orc', 80, 16, 80]
    mummy = ['mummy', 160, 32, 160]
    quimera = ['quimera', 320, 64, 320]
    dragon = ['dragon', 1000, 100, 1000]

    if player_level < 5: 
        return random.choice([slime, goblin, troll])
    elif player_level < 10:
        return random.choice([orc, mummy, quimera])
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
        return 0, False # Defender died
    else:
        return defender_hp, True # Defender is alive

# 6. Function to calculate level up
def calculate_level(player_lv, player_exp, player_hp, player_force, monster_exp):
    player_exp = player_exp + monster_exp
    required_exp = 3 ** player_lv

    if player_exp >= required_exp: # Check if exp is enough to level up
        print('Level Up!')
        player_lv += 1
        player_hp = 100
        player_force = player_force * 2

    return player_lv, player_exp, player_hp, player_force