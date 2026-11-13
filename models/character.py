from dataclasses import dataclass
import random

@dataclass
class Character:
    name: str
    hp: int
    max_exp: int 
    strength: int

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def attack(self, target: 'Character') -> int:
        attacker_luck = random.randint(0, 6)
        defender_luck = random.randint(0, 6)
        damage = (self.strength * attacker_luck) - (target.strength * defender_luck)

        if damage > 0:
            target.take_damage(damage)
            return damage
        return 0