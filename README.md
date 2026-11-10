# Fibula RPG

```
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
```

A text-based RPG for the terminal, written in Python. Name your hero, fight random monsters, level up, find potions and see how far you can get before the game is over.

This project was built while following the **Universo Discreto** tutorials by Lucas Lattari, as a way to practice core Python concepts. The original project is [lucaslattari/fibula_rpg](https://github.com/lucaslattari/fibula_rpg/).

## How to run

You only need Python 3 installed. There are no external dependencies.

```bash
git clone https://github.com/<your-username>/fibula-rpg.git
cd fibula-rpg
python fibula_rpg.py
```
## Documentation & Architecture

All the engineering planning, database modeling, and architectural decisions for this project are fully documented:

- 📖 [Access Full Documentation on Google Docs](Yhttps://docs.google.com/document/d/1kBHUqnA7eby_nga2Mo1MH0krLE2cQ65YVrwrmnBsZ58/edit?usp=sharing)

### What's inside the documentation:
- **Overview & Architecture:** High-level project design and layered architecture principles.
- **System Design:** Breakdown of layers (UI, Controllers, Services, Repositories).
- **Python & Logic:** Applied core concepts and clean code standards.
- **Database Modeling:** Relational schema (`players`, `items`, `inventory`) and SQL queries.
- **REST APIs & Git/GitHub:** Communication patterns and version control workflows.


## How to play

When the game starts you enter your hero's name, and a monster appears. On each turn you pick an action:

| Option | Action | What it does |
| --- | --- | --- |
| 1 | Attack | Attack the monster. If it survives, it strikes back. |
| 2 | Use item | Open your inventory and use an item (for example, a potion). |
| 3 | Run away | 50% chance to escape. If you fail, the monster attacks. |
| 4 | View status | Show HP, level, EXP, strength and inventory. |
| 5 | Quit game | End the game. |

## Game mechanics

### Starting stats

| Attribute | Value |
| --- | --- |
| HP | 100 |
| Level | 1 |
| Strength | 3 |
| EXP | 0 |
| Inventory | empty |
| Status | alive |

### Combat

Each attack rolls a random "luck" value from 0 to 6 for both the attacker and the defender:

```
damage = attacker_strength * attacker_luck - defender_strength * defender_luck
```

- Luck of 6 is a **critical hit**.
- Luck of 0 means the attacker **missed**.
- If the damage is zero or negative, the defender takes no damage.

### Monsters

The monster you face depends on your level:

| Your level | Possible monsters |
| --- | --- |
| 1 to 4 | Slime, Goblin, Troll |
| 5 to 9 | Orc, Mummy, Chimera |
| 10+ | Dragon |

Each monster has a name, HP, strength and the EXP it gives when defeated.

### Leveling up

Defeating a monster gives you EXP. When your EXP reaches `3 ** level`, you level up:

- HP is fully restored.
- Strength is doubled.

### Items

After a victory there is a chance to receive a **Potion**. Using a potion restores 20 HP, up to a maximum of 100.

### Game over

The game ends when your HP reaches 0 or when you choose to quit.

## Python concepts practiced

- Importing modules (`import random`)
- Strings, `print`, multi-line and raw strings (for the ASCII art)
- Functions with parameters and return values (`def`, `return`)
- Variables and basic types (`str`, `int`, `list`, `bool`)
- User input with `input()`
- Conditionals (`if`, `elif`, `else`)
- Loops (`while`)
- Lists: adding, removing and iterating over items
- Random numbers (`random.choice()`, `random.randint()`, `random.random()`)
- f-strings
- Program entry point (`if __name__ == "__main__":`)

## Ideas for the future

- Refactor the player and monsters into classes (object-oriented programming)
- Save and load the game using files
- More items, monsters and special attacks

## Credits

Based on the Fibula RPG tutorial by [Lucas Lattari](https://github.com/lucaslattari) (Universo Discreto).