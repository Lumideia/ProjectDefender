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
    hp: int
    armour: int
    ablative: int
    movement: int
    view: int
    dodge: int
    accuracy: int
    explosion_resistance: int
    is_organic: bool
    throw_distance: int
    size: CharacterSize
    main_weapon: WeaponInstance
    side_weapon: WeaponInstance = None
