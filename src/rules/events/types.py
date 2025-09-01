from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Protocol

from src.rules.characters.character import Character
from src.rules.weapons.weapon import Weapon


# Could be used later

# class HasHP(Protocol):
#     hp: int
#
# class HasWeapon(Protocol):
#     pass

class Event(Enum):
    TURN_START = auto()
    TURN_END = auto()
    ON_HIT = auto()
    ON_DAMAGE_TAKEN = auto()
    ON_KILL = auto()
    ON_MOVE = auto()

@dataclass
class EventCtx(ABC):
    pass

@dataclass
class TurnCtx:
    actor: Character

@dataclass
class HitCtx:
    attacker: Character
    target: Character
    distance: int
    weapon: Optional[Weapon] = None
