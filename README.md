# Fibula RPG

```text
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

A text-based RPG for the terminal, written in Python, styled with **Rich** for dark retro panels, progress bars, sound effects, and a lo-fi holiday easter egg. Name your hero, start a new adventure or load a saved run, battle monsters, level up, use potions, and see how far you can go before game over.

This project was built while following the **Universo Discreto** tutorials by Lucas Lattari, as a way to practice core Python concepts and expand the project into a full CLI + API experience. The original project is [lucaslattari/fibula_rpg](https://github.com/lucaslattari/fibula_rpg/).

## CLI Preview

> Full walkthrough of the terminal experience built with `Rich`, including the title screen, `New Game` / `Load Game` persistence with SQLite, combat loop, the `xmas` lo-fi easter egg, and the `Game Over` screen.

<video src="assets/fibula_rpg_demo.mp4" controls width="100%"></video>

## How to run

Make sure Python 3 and `rich` are installed, then run `main.py` from the project root:

```bash
git clone https://github.com/gabdorada/fibula-rpg.git
cd fibula-rpg
pip install rich
python main.py
```

## Documentation & Architecture

All the engineering planning, database modeling, and architectural decisions for this project are fully documented:

- 📖 [Access Full Documentation on Notion](https://agreeable-angle-6cf.notion.site/Fibula-RPG-Documenta-o-41d537a4adae8020b613db24800b908e?source=copy_link)

### What's inside the documentation:
- **Overview & Architecture:** High-level project design and layered architecture principles.
- **System Design:** Breakdown of layers (UI, Controllers, Services, Repositories).
- **Python & Logic:** Applied core concepts and clean code standards.
- **Database Modeling:** Relational schema (`players`, `items`, `inventory`) and SQL queries.
- **REST APIs & Git/GitHub:** Communication patterns and version control workflows.

## How to play

When the game starts, you can choose **New Game** or **Load Game** (using your hero's name to restore saved progress from the database). On each turn, a wild monster appears and you choose an action:

| Option | Action | What it does |
| --- | --- | --- |
| 1 | Attack | Attack the current monster. If it survives, it strikes back. |
| 2 | Use item | Open your inventory and choose an item (such as a potion) to use. |
| 3 | Run away | Attempt to escape from the current encounter. If escape fails, the monster attacks. |
| 4 | View status | Show a status panel with HP, level, EXP (and EXP remaining to level up), strength, and inventory count. |
| 5 | Quit game | Trigger the game over summary screen and exit. |

> **Hidden command:** Type `xmas` at the action prompt to open the blinking Christmas tree easter egg with lo-fi audio (on supported macOS terminals with `afplay`), and press `x` (or `X`) to close it immediately.

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

### Combat & Progression

- **Combat & HUD:** Combats resolve attacks and counterattacks between player and monster, updating HP/XP bars and sound feedback (`console.bell()` and non-blocking `afplay` sounds when available).
- **Monsters:** Spawns monsters scaled to the player's level (`Monster.spawn_for_level(player.level)`), with HP, strength, and EXP rewards.
- **Leveling up & Loot:** Defeating a monster grants EXP toward leveling up and has a chance to drop a **Potion** (`+20 HP`) into your inventory.
- **Game over:** Happens when your HP reaches `0` or when you choose to quit (`5`), displaying a centered summary panel with your final stats.

## Python concepts practiced

- Importing standard library modules (`math`, `os`, `random`, `shutil`, `struct`, `subprocess`, `sys`, `tempfile`, `termios`, `threading`, `time`, `tty`, `wave`) and third-party UI tools (`rich`)
- Terminal UI layout and live rendering (`Console`, `Panel`, `Align`, `Group`, `Text`, `Live`)
- Background threads, synchronization events (`threading.Event`), temporary WAV synthesis, and raw/cbreak terminal key listening (`termios`, `tty`)
- Functions, classes, type hints, conditionals, loops, lists, f-strings, and `if __name__ == "__main__":`

## Ideas for the future

- Expand REST API endpoints (`feat/fastapi`) integrated with the shared SQLite persistence layer
- Add more items, monsters, and combat actions
- Add cross-platform audio support beyond macOS `afplay`

## Credits

Based on the Fibula RPG tutorial by [Lucas Lattari](https://github.com/lucaslattari) (Universo Discreto).
