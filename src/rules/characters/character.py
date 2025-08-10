from abc import ABC
from enum import Enum

class CharacterSize(Enum):
    SMALL = 1
    MEDIUM = 2
    HUGE = 3


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

    # TODO: Logic to apply modifiers on self/enemies state (effects)