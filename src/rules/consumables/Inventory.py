from dataclasses import dataclass, field
from typing import List, Optional

from src.rules.consumables.InventoryCell import InventoryCell, TypedInventoryCell, GenericInventoryCell
from src.rules.consumables.consumable import Consumable, DEFAULT_CONSUMABLES

MAX_CELLS = 24  # TODO: Move to global settings

@dataclass
class Inventory:
    space: int = 2
    cells: List[InventoryCell] = field(default_factory=lambda: [
        GenericInventoryCell(), GenericInventoryCell(),
        *[InventoryCell() for _ in range(MAX_CELLS - 2)]
    ])

    def _sort_cells(self):
        def cell_sort_key(cell: InventoryCell) -> int:
            if isinstance(cell, GenericInventoryCell):
                return 0
            elif isinstance(cell, TypedInventoryCell):
                return 1
            return 2

        self.cells.sort(key=cell_sort_key)

    def get_consumable_by_name(self, name: str) -> Optional[Consumable]:
        cls = next((p for p in DEFAULT_CONSUMABLES if p.class_name == name), None)
        return cls() if cls else None

    def get_consumable_count(self, name: str) -> int:
        return sum(
            1 for cell in self.cells
            if cell.consumable and cell.consumable.class_name == name
        )

    def use_by_name(self, name: str) -> bool:
        for cell in self.cells:
            if isinstance(cell, GenericInventoryCell) and cell.consumable and cell.consumable.class_name == name:
                cell.pick_consumable().apply()
                return True

        for cell in self.cells:
            if not isinstance(cell, GenericInventoryCell) and cell.consumable and cell.consumable.class_name == name:
                cell.pick_consumable().apply()
                return True

        return False

    def add_by_name(self, name: str) -> bool:
        consumable = self.get_consumable_by_name(name)
        if consumable:
            return self._add_consumable(consumable)
        return False

    def _add_consumable(self, consumable: Consumable) -> bool:
        for cell in self.cells:
            if isinstance(cell, TypedInventoryCell) and cell.check_if_available(consumable) and not cell.consumable:
                cell.put_consumable(consumable)
                return True

        for cell in self.cells:
            if isinstance(cell, GenericInventoryCell) and not cell.consumable:
                cell.put_consumable(consumable)
                return True

        return False

    def add_cell(self, cell: InventoryCell) -> InventoryCell:
        for i, existing in enumerate(self.cells):
            if type(existing) is InventoryCell:
                self.cells[i] = cell
                self._sort_cells()
                return cell

        raise ValueError("No replaceable cell found")

    def add_to_specific_cell(self, cell: InventoryCell, consumable: Consumable) -> bool:
        if cell in self.cells and not cell.consumable and cell.check_if_available(consumable):
            cell.put_consumable(consumable)
            return True
        return False
