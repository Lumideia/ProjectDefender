from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from src.enteties.weapon_instance import WeaponInstance

class CharacterSize(Enum):
    SMALL = 1
    MEDIUM = 2
    HUGE = 3


@dataclass
class Character(ABC):
    hp: int = 40
    armour: int = 1
    ablative: int = 3
    movement: int = 40
    view: int = 30
    dodge: int = 0
    accuracy: int = 0
    explosion_resistance: int = 0
    is_organic: bool = True
    throw_distance: int = 40
    size: CharacterSize = CharacterSize.MEDIUM
