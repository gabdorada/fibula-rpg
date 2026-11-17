from dataclasses import dataclass, field
from models.character import Character
from models.item import Item

@dataclass
class Player(Character):
    level: int = 1
    exp: int = 0
    inventory = list[Item] = field(default_factory=list)

    @property
    def required_exp(self) -> int:
        return 3 ** self.level
    
    def heal(self, amount: int) -> None:
        self.hp = min(self.max_exp, self.hp + amount)

    def add_item(self, item: Item) -> None:
        self.inventory.append(item)

    def use_item(self, index: int) -> bool:
        if 0 <= index < len(self.inventory):
            item = self.inventory.pop(index)
            if item.item_type == 'potion':
                self.heal(item.effect_value)
                return True
        return False

    def gain_exp(self, amount: int) -> bool:
        self.exp += amount
        leveled_up = False
        while self.exp >= self.required_exp:
            self.level += 1
            self.hp = 100
            self.strength *= 2
            leveled_up = True
        return leveled_up