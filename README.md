# Fibula RPG

```text
         \ _^ /   ,^,
         \>@@</   ((
Art by    (..)    );)
 Charles   vv\^^^^ /
 Caffrey /==   ))) )
         ( ==/ )=< \
         {{{)=(}}}(_}}}
```

A terminal-based Python RPG. A quiet exercise in finding structure amidst the noise of loose variables and turning draft ideas into actual instances.

Based on the study materials and repository by [Lucas Lattari](https://github.com/lucaslattari/fibula_rpg_poo).

> 🎯 **Project Purpose & Playground**:
> This is my main sandbox project for experimenting with advanced Python features, `dataclasses`, algorithms, data structures, and software architecture concepts as I learn them.

## The Process

Writing code often feels like drawing on a blank page: we start with quick, messy sketches until we feel the need to trace clearer margins.

This repository tracks the transition from a simple structured script to Object-Oriented Programming (OOP):

- **Initial Chaos:** Loose variables, scattered combat data, and duplicated logic between player and monsters.
- **Dictionaries:** An attempt to label drawers and organize raw data—useful for storing information, but insufficient for managing actions and behaviors.
- **Structure (OOP):** Encapsulating data and actions inside the same entity. Using the base class `Entity` to set the rules of life and damage, leaving `Player` and `Monster` to hold only what makes them distinct.

## Code Notebook Structure

```text
fibula_rpg/
│
├── entities/
│   ├── entity.py       # The foundation: health, damage, and attacking
│   ├── player.py       # The player: inventory, experience, and levels
│   └── monster.py      # The encounters along the way
│
├── utils/
│   └── combat.py       # Where actions meet and turns unfold
│
├── main.py             # The starting point
└── .gitignore          # Keeping temporary noise out of the repo
```

## How to Run

```bash
python main.py
```