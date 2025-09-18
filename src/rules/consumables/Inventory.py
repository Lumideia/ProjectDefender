from dataclasses import dataclass, field
from typing import List, Dict

from src.rules.consumables.consumable import Consumable, DEFAULT_CONSUMABLES


@dataclass
class Inventory:
    space: int = 2
    # ключ — строка (class_name), значение — количество
    consumables: Dict[str, int] = field(default_factory=dict)

    def get_consumables(self, name) -> Consumable:
        cls = next((p for p in DEFAULT_CONSUMABLES if p.class_name == name), None)
        return cls() if cls else None

    def add_consumable(self, name: str) -> None:
        consumable = self.get_consumables(name)
        current_total = sum(self.consumables.values())
        current_for_item = self.consumables.get(name, 0)
        max_count = consumable.max_count or self.space

        if current_total < self.space and current_for_item < max_count:
            self.consumables[name] = current_for_item + 1

    def use_consumable(self, name: str) -> None:
        consumable = self.get_consumables(name)
        if name in self.consumables:
            consumable.apply()
            self.consumables[name] -= 1
            if self.consumables[name] <= 0:
                self.consumables.pop(name)
