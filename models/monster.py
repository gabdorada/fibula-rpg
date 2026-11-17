from dataclasses import dataclass
from models.character import Character
import random

@dataclass
class Monster(Character):
    exp_reward: int = 0

    @classmethod
    def spawn_fo_level(cls, player_level: int) -> "Monster":
        if player_level < 5:
            pool = [
                cls(name='Slime', hp=20, max_exp=20, strength=2, exp_reward=2),
                cls(name='Goblin', hp=35, max_exp=35, strength=4, exp_reward=4),
                cls(name='Troll', hp=50, max_exp=50, strength=6, exp_reward=6),
            ]
        elif player_level < 10:
            pool = [
                cls(name='Orc', hp=80, max_exp=80, strength=12, exp_reward=15),
                cls(name='Mummy', hp=100, max_exp=100, strength=15, exp_reward=20),
                cls(name='Chimera', hp=130, max_exp=130, strength=18, exp_reward=25),
            ]
        else:
            pool = [
                cls(name='Dragon', hp=250, max_exp=250, strength=35, exp_reward=100)
            ]

        return random.choice(pool)