# Fibula RPG

```
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

## Project Purpose

This is my main sandbox project for experimenting with advanced Python features, `dataclasses`, algorithms, data structures, and software architecture concepts as I learn them.

## Learning Log

Every time I learn or apply a new concept here, I write it down in the project's Google Doc, in the **Updates** tab (in Portuguese and English).

👉 **[Fibula RPG: Learning Log (Google Docs)](https://docs.google.com/document/d/1LdQNg0swxYVUlgp80CpBRyLTqq4uW5Pzk4pklOxin2c/edit?usp=sharing)**

What I'm working on or planning to apply:

- [ ] Refactor `Entity`, `Player` and `Monster` with `@dataclass`
- [ ] Clean up the project structure and imports
- [ ] Algorithms
- [ ] Data structures

## The Process

Writing code often feels like drawing on a blank page: we start with quick, messy sketches until we feel the need to trace clearer margins.

This repository tracks the transition from a simple structured script to Object-Oriented Programming (OOP):

- **Initial Chaos:** loose variables, scattered combat data, and duplicated logic between player and monsters.
- **Dictionaries:** an attempt to label drawers and organize raw data. Useful for storing information, but insufficient for managing actions and behaviors.
- **Structure (OOP):** encapsulating data and actions inside the same entity. The base class `Entity` sets the rules of life and damage, leaving `Player` and `Monster` to hold only what makes them distinct.

## Code Notebook Structure

```
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
├── index.html          # Web frontend (single file)
└── .gitignore          # Keeping temporary noise out of the repo
```

## How to Run

Terminal version:

```
python main.py
```

## Credits

- Study materials and base repository by [Lucas Lattari](https://github.com/lucaslattari/fibula_rpg_poo) (Universo Discreto).
- ASCII art by Charles Caffrey.