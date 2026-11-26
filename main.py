import math
import os
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import termios
import threading
import time
import tty
import wave

from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from database import Database
from models import Item, Monster, Player

console = Console()


def _play_sfx(sound_file: str | None = None):
    """Play a non-blocking terminal bell or macOS system sound if available."""
    try:
        console.bell()
    except Exception:
        pass

    if sound_file and sys.platform == "darwin" and shutil.which("afplay"):
        def _run():
            try:
                subprocess.run(
                    ["afplay", sound_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            except Exception:
                pass

        threading.Thread(target=_run, daemon=True).start()


def _render_lofi_wav(notes_hz: list[tuple[float, float]], sample_rate: int = 22050) -> str:
    """Generate a temporary warm lo-fi WAV file (soft sine + low-pass + subtle tape warmth)."""
    fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)

    samples: list[float] = []
    rng = random.Random(42)

    for freq, duration in notes_hz:
        n_samples = max(1, int(sample_rate * duration))
        attack = max(1, int(sample_rate * 0.03))
        release = max(1, int(sample_rate * 0.08))

        for i in range(n_samples):
            t = i / sample_rate
            wave_val = 0.75 * math.sin(2 * math.pi * freq * t) + 0.15 * math.sin(
                2 * math.pi * (freq * 2.0) * t
            )
            tape_hiss = 0.012 * rng.uniform(-1.0, 1.0)

            env = 1.0
            if i < attack:
                env = i / attack
            elif i > n_samples - release:
                env = max(0.0, (n_samples - i) / release)

            samples.append((wave_val * env) + tape_hiss)

    alpha = 0.14
    filtered: list[float] = []
    prev = 0.0
    for s in samples:
        prev = prev + alpha * (s - prev)
        filtered.append(prev * 0.45)

    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        pcm = bytearray()
        for val in filtered:
            clamped = max(-1.0, min(1.0, val))
            pcm.extend(struct.pack("<h", int(clamped * 32767)))
        wf.writeframes(bytes(pcm))

    return wav_path


def _play_lofi_sequence(
    notes_hz: list[tuple[float, float]],
    stop_event: threading.Event | None = None,
):
    """Play a lo-fi sequence with afplay on macOS and clean up the temp file."""
    if sys.platform != "darwin" or not shutil.which("afplay"):
        return

    wav_path = _render_lofi_wav(notes_hz)
    proc = None
    try:
        proc = subprocess.Popen(
            ["afplay", wav_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        total_time = sum(d for _, d in notes_hz) + 0.1
        elapsed = 0.0
        while elapsed < total_time:
            if stop_event is not None and stop_event.is_set():
                break
            time.sleep(0.05)
            elapsed += 0.05
    finally:
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
            except Exception:
                pass
        try:
            if os.path.exists(wav_path):
                os.remove(wav_path)
        except Exception:
            pass


def _play_xmas_jingle(stop_event: threading.Event):
    """Play a cozy, laid-back lo-fi holiday progression until 'x' is pressed."""
    lofi_xmas_notes = [
        (349.23, 0.36),  # F4
        (440.00, 0.34),  # A4
        (523.25, 0.38),  # C5
        (659.25, 0.50),  # E5
        (329.63, 0.36),  # E4
        (392.00, 0.34),  # G4
        (493.88, 0.38),  # B4
        (587.33, 0.50),  # D5
        (293.66, 0.36),  # D4
        (349.23, 0.34),  # F4
        (440.00, 0.38),  # A4
        (523.25, 0.50),  # C5
        (261.63, 0.42),  # C4
        (329.63, 0.40),  # E4
        (392.00, 0.42),  # G4
        (493.88, 0.65),  # B4
    ]
    _play_lofi_sequence(lofi_xmas_notes, stop_event=stop_event)


def _make_bar(current: int, maximum: int, width: int = 18, mode: str = "hp") -> str:
    safe_max = max(maximum, 1)
    ratio = max(0.0, min(1.0, current / safe_max))
    filled = round(ratio * width)
    empty = width - filled

    if mode == "xp":
        color = "cyan"
    elif mode == "dead":
        color = "red"
    else:
        if ratio > 0.5:
            color = "green"
        elif ratio > 0.25:
            color = "yellow"
        else:
            color = "red"

    bar = f"[bold {color}]{'█' * filled}[/bold {color}][dim]{'░' * empty}[/dim]"
    return f"{bar} [bold {color}]{max(current, 0)}/{maximum}[/bold {color}]"


# 1. Function to display the opening title (centered)
def show_title():
    title_lines = [
        r"                \||/                ",
        r"                |  @___oo           ",
        r"      /\  /\   / (__,,,,|          ",
        r"     ) /^\) ^\/ _)                  ",
        r"     )   /^\/   _)                  ",
        r"     )   _ /  / _)                  ",
        r" /\  )/\/ ||  | )_)                 ",
        r"<  >      |(,,) )__)                ",
        r" ||      /    \)___)\               ",
        r" | \____(      )___) )___           ",
        r"  \______(_______;;; __;;;          ",
    ]
    art = Group(*(Align.center(Text(line, style="bold white")) for line in title_lines))
    subtitle = Align.center(
        Text.from_markup(
            "\n[bold white]F I B U L A   R P G[/bold white]\n"
            "[dim]~ a dark little dungeon ~[/dim]"
        )
    )
    console.print()
    console.print(
        Align.center(
            Panel(
                Group(art, subtitle),
                border_style="bright_black",
                expand=False,
                padding=(0, 4),
            )
        )
    )


# Christmas Easter Egg (centered, blinking tree until pressing 'x')
def _build_tree_panel(phase: int) -> Panel:
    palettes = [
        ("yellow", "green", "red"),
        ("red", "yellow", "green"),
        ("green", "red", "yellow"),
    ]
    c1, c2, c3 = palettes[phase % len(palettes)]

    def make_line(parts: list[tuple[str, str]]) -> Text:
        t = Text()
        for text_part, style in parts:
            t.append(text_part, style=style)
        return t

    rows = [
        make_line([("*", f"bold {c1}")]),
        make_line([("/", "dim"), ("o", f"bold {c2}"), ("\\", "dim")]),
        make_line([("/_", "dim"), ("o", f"bold {c3}"), ("_\\", "dim")]),
        make_line([("/", "dim"), ("o", f"bold {c1}"), ("___", "dim"), ("o", f"bold {c2}"), ("\\", "dim")]),
        make_line([("/___", "dim"), ("o", f"bold {c3}"), ("___\\", "dim")]),
        make_line([("/", "dim"), ("o", f"bold {c2}"), ("___", "dim"), ("o", f"bold {c1}"), ("\\", "dim")]),
        make_line([("/___", "dim"), ("o", f"bold {c3}"), ("___", "dim"), ("o", f"bold {c2}"), ("___\\", "dim")]),
        make_line([
            ("/", "dim"),
            ("o", f"bold {c1}"),
            ("___", "dim"),
            ("o", f"bold {c2}"),
            ("___", "dim"),
            ("o", f"bold {c3}"),
            ("___", "dim"),
            ("o", f"bold {c1}"),
            ("\\", "dim"),
        ]),
        make_line([("/____", "dim"), ("o", f"bold {c2}"), ("___", "dim"), ("o", f"bold {c3}"), ("_____\\", "dim")]),
        make_line([("   |||", "dim")]),
    ]

    tree_group = Group(*(Align.center(row) for row in rows))

    footer_t1 = Align.center(Text("~ Merry Christmas ~", style="bold white"))
    footer_t2 = Align.center(Text("may your HP always be full", style="dim"))
    footer_t3 = Align.center(
        Text.assemble(("press ", "dim"), ("x", "bold white"), (" to close", "dim"))
    )

    return Panel(
        Group(tree_group, Text(""), footer_t1, footer_t2, footer_t3),
        border_style="bright_black",
        expand=False,
        padding=(1, 6),
    )


def _wait_for_x_key(stop_event: threading.Event):
    """Wait until the user presses 'x' or 'X'."""
    if not sys.stdin.isatty():
        while not stop_event.is_set():
            typed = console.input().strip().lower()
            if typed == "x":
                stop_event.set()
                break
        return

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while not stop_event.is_set():
            ch = sys.stdin.read(1)
            if ch and ch.lower() == "x":
                stop_event.set()
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def show_christmas_easter_egg(delay: float = 0.25):
    stop_event = threading.Event()
    listener = threading.Thread(target=_wait_for_x_key, args=(stop_event,), daemon=True)
    jingle = threading.Thread(target=_play_xmas_jingle, args=(stop_event,), daemon=True)
    listener.start()
    jingle.start()

    phase = 0
    try:
        with Live(
            Align.center(_build_tree_panel(phase)),
            console=console,
            refresh_per_second=8,
            transient=True,
        ) as live:
            while not stop_event.is_set():
                time.sleep(delay)
                phase += 1
                live.update(Align.center(_build_tree_panel(phase)))
    finally:
        stop_event.set()
        listener.join(timeout=0.2)
        jingle.join(timeout=0.2)


# 2. Function to display game over (centered)
def game_over(player: Player | None = None, reason: str | None = None):
    _play_sfx("/System/Library/Sounds/Basso.aiff")
    skull_lines = [
        r"   .-''''''-.   ",
        r"  /   _  _   \  ",
        r" |   (o)(o)   | ",
        r" \     ^      / ",
        r"  |  ||||||  |  ",
        r"  '----------'  ",
    ]
    skull_block = Group(*(Align.center(Text(line, style="bold white")) for line in skull_lines))

    header_parts = ["\n[bold red]G A M E   O V E R[/bold red]"]
    if reason:
        header_parts.append(f"[dim]{reason}[/dim]")
    header = Align.center(Text.from_markup("\n".join(header_parts)))

    stats_renderable = None
    if player is not None:
        max_hp = getattr(player, "max_hp", 100)
        potions_left = sum(
            1 for item in getattr(player, "inventory", [])
            if getattr(item, "item_type", "") == "potion"
        )
        hp_line = Align.center(
            Text.from_markup(f"\n[dim]HP[/dim]  {_make_bar(0, max_hp, width=16, mode='dead')}")
        )
        meta_line = Align.center(
            Text.from_markup(
                f"[dim]Hero[/dim] [bold white]{player.name}[/bold white]   "
                f"[dim]Level[/dim] [bold white]{player.level}[/bold white]   "
                f"[dim]Potions left[/dim] [bold white]{potions_left}[/bold white]"
            )
        )
        stats_renderable = Group(hp_line, meta_line)

    footer = Align.center(Text.from_markup("\n[dim]Thanks for playing.[/dim]"))

    parts = [skull_block, header]
    if stats_renderable is not None:
        parts.append(stats_renderable)
    parts.append(footer)

    console.print()
    console.print(
        Align.center(
            Panel(
                Group(*parts),
                border_style="red",
                expand=False,
                padding=(1, 5),
            )
        )
    )
    raise SystemExit(1)


# 3. Generic Combat Function (uses methods from the Character class)
def handle_combat(attacker, defender):
    hp_before = defender.hp
    damage = attacker.attack(defender)
    actual_damage = max(0, hp_before - defender.hp) if damage is None else max(0, damage)

    if actual_damage > 0:
        console.print(
            f"[bold white]{attacker.name}[/bold white] hits "
            f"[bold white]{defender.name}[/bold white] for [bold red]{actual_damage}[/bold red]"
        )
        if isinstance(defender, Player):
            _play_sfx()
    else:
        console.print(f"[dim]{attacker.name} misses {defender.name}![/dim]")

    if not defender.is_alive:
        console.print(f"[bold red]{defender.name} died![/bold red]")
        return False
    return True


def _show_hud(player: Player, monster: Monster | None = None):
    max_hp = getattr(player, "max_hp", 100)
    req_exp = getattr(player, "required_exp", 100)

    if monster is not None and monster.is_alive:
        monster_max_hp = getattr(monster, "max_hp", monster.hp)
        console.print(
            f"  [dim]— a wild[/dim] [bold white]{monster.name}[/bold white] "
            f"[dim]appears!  HP[/dim] {_make_bar(monster.hp, monster_max_hp, width=10, mode='hp')}"
        )

    console.print(f"[bold white]{player.name}[/bold white]  [dim]LV {player.level}[/dim]")
    console.print(f"[dim]HP[/dim]  {_make_bar(player.hp, max_hp, width=18, mode='hp')}")
    console.print(f"[dim]XP[/dim]  {_make_bar(player.exp, req_exp, width=18, mode='xp')}")


# 4. Main Game Function
def main():
    show_title()
    db = Database()

    # Game Load or New Game Choice
    console.print()
    console.print("  [dim]1.[/dim] New Game")
    console.print("  [dim]2.[/dim] Load Game")
    choice = console.input("\n[bold white]>[/bold white] ").strip()

    player = None
    if choice == "2":
        hero_name = console.input("[bold white]Enter your saved heroine/hero name:[/bold white] ").strip()
        player = db.load_player(hero_name)
        if not player:
            console.print("[yellow]Character not found! Creating a new game...[/yellow]")
        else:
            console.print("[dim]save loaded.[/dim]")

    if not player:
        hero_name = console.input("[bold white]Enter the name of your heroine/hero:[/bold white] ").strip()
        player = Player(name=hero_name or "Adventurer", hp=100, max_exp=100, strength=3)

    # Save initial state to database
    db.save_player(player)
    console.print()

    current_monster = None

    while True:
        # If there is no active monster, generate a new one based on the player's level
        if current_monster is None or not current_monster.is_alive:
            current_monster = Monster.spawn_for_level(player.level)
            console.print()
            _show_hud(player, current_monster)
        else:
            console.print()
            _show_hud(player)

        console.print()
        console.print("  [dim]1.[/dim] Attack")
        console.print(f"  [dim]2.[/dim] Use item [dim]({len(player.inventory)})[/dim]")
        console.print("  [dim]3.[/dim] Run away")
        console.print("  [dim]4.[/dim] View status")
        console.print("  [dim]5.[/dim] Quit game")

        raw_option = console.input("\n[bold white]>[/bold white] ").strip().lower()
        console.print()

        if raw_option == "xmas":
            show_christmas_easter_egg()
            continue

        try:
            option = int(raw_option)
        except ValueError:
            console.print("[yellow]Invalid option![/yellow]")
            continue

        if option == 1:
            # Player's Turn
            monster_survived = handle_combat(player, current_monster)

            if monster_survived:
                # Monster's Turn (Counterattack)
                player_survived = handle_combat(current_monster, player)
                if not player_survived:
                    game_over(player, reason=f"slain by a {current_monster.name}")
                else:
                    # Monster defeated: EXP reward
                    console.print(f"[bold cyan]+{current_monster.exp_reward} XP[/bold cyan]")
                    leveled_up = player.gain_exp(current_monster.exp_reward)
                    if leveled_up:
                        _play_sfx("/System/Library/Sounds/Glass.aiff")
                        console.print(
                            f"[bold blue]Level Up![/bold blue] now level [bold white]{player.level}[/bold white]"
                        )

                    # Chance to drop a potion (Item)
                    if random.random() <= 0.5:  # 50% chance of loot
                        potion = Item(name="Potion", item_type="potion", effect_value=20)
                        player.add_item(potion)
                        _play_sfx("/System/Library/Sounds/Glass.aiff")
                        console.print("[green]You got a Potion![/green]")

                    current_monster = None  # Need to generate a new monster in the next round

        elif option == 2:
            # Use item from inventory
            if not player.inventory:
                console.print("[dim]Your inventory is empty.[/dim]")
            else:
                console.print("[bold white]Inventory:[/bold white]")
                for index, item in enumerate(player.inventory):
                    console.print(
                        f"  [dim]{index + 1}.[/dim] {item.name} [green](+{item.effect_value} HP)[/green]"
                    )

                try:
                    item_potion = int(
                        console.input("[bold white]Choose an item (or 0 to cancel):[/bold white] ").strip()
                    )
                except ValueError:
                    console.print("[yellow]Invalid item choice.[/yellow]")
                    continue

                if item_potion > 0:
                    _play_sfx("/System/Library/Sounds/Glass.aiff")
                    console.print(
                        f"[green]You used a potion.[/green] Your HP is now [bold white]{player.hp}[/bold white]"
                    )
                else:
                    console.print("[dim]Invalid item choice.[/dim]")

        elif option == 3:
            # Attempt to escape (50% chance)
            success = random.choice([True, False])
            if success:
                console.print(f"[dim]{player.name} escaped successfully![/dim]")
                current_monster = None  # Resets the current monster
            else:
                console.print(f"[yellow]{player.name} could not escape![/yellow]")
                # Monster attacks if escape fails
                player_survived = handle_combat(current_monster, player)
                if not player_survived:
                    game_over(player, reason=f"slain by a {current_monster.name}")

        elif option == 4:
            # View detailed status
            max_hp = getattr(player, "max_hp", 100)
            status_body = (
                f"[dim]HP[/dim]     [bold white]{player.hp}/{max_hp}[/bold white]\n"
                f"[dim]LV[/dim]     [bold white]{player.level}[/bold white]\n"
                f"[dim]EXP[/dim]    [bold white]{player.exp} / {player.required_exp}[/bold white]  "
                f"[dim]({max(0, player.required_exp - player.exp)} to level up)[/dim]\n"
                f"[dim]STR[/dim]    [bold white]{player.strength}[/bold white]\n"
                f"[dim]Items[/dim]  [bold white]{len(player.inventory)}[/bold white]"
            )
            console.print(
                Panel(
                    status_body,
                    title=f"=== {player.name} Status ===",
                    title_align="left",
                    border_style="bright_black",
                    expand=False,
                    padding=(0, 2),
                )
            )

        elif option == 5:
            game_over(player, reason="saved. see you in the dark.")
        else:
            console.print("[yellow]Invalid option![/yellow]")


if __name__ == "__main__":
    main()