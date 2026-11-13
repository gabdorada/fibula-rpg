from dataclasses import dataclass

@dataclass(frozen=True)
class Item:
    name: str
    item_type: str          # ex: 'potion', 'weapon'
    effect_value = int 