from dataclasses import dataclass, field
from typing import List, Optional, Type

from src.rules.consumables.consumable import Consumable, Grenade


@dataclass
class InventoryCell:
    is_active: bool = False
    available_consumables: List[Type[Consumable]] = field(default_factory=list)
    consumable: Optional[Consumable] = None

    def check_if_available(self, consumable: Consumable) -> bool:
        pass

    def put_consumable(self, consumable: Consumable) -> bool:
        if not self.consumable and self.check_if_available(consumable):
            self.consumable = consumable
            return True
        return False

    def pick_consumable(self):
        consumable = self.consumable
        self.consumable = None
        return consumable

@dataclass
class GenericInventoryCell(InventoryCell):
    def check_if_available(self, consumable: Consumable) -> bool:
        return True

@dataclass
class TypedInventoryCell(InventoryCell):
    def check_if_available(self, consumable: Consumable) -> bool:
        return any(isinstance(consumable, av) for av in self.available_consumables)

@dataclass
class GrenadeOnlyCell(TypedInventoryCell):
    available_consumables: List[Type[Consumable]] = field(default_factory=lambda: [Grenade])
