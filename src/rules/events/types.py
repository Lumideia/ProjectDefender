from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple

from src.enteties.character_instance import CharacterInstance
from src.enteties.weapon_instance import WeaponInstance


class Event(Enum):
    TURN_START = auto()
    TURN_END = auto()
    ON_HIT = auto()
    ON_DAMAGE_TAKEN = auto()
    ON_KILL = auto()
    ON_MOVE = auto()

@dataclass(frozen=True)
class EventCtx:
    pass

@dataclass(frozen=True)
class CharacterEvent(EventCtx):
    actor: CharacterInstance

@dataclass(frozen=True)
class MoveCtx(CharacterEvent):
    start_pos: Tuple[int, int]
    end_pos: Tuple[int, int]

@dataclass(frozen=True)
class HitCtx(CharacterEvent):
    target: CharacterInstance
    distance: int
    weapon: Optional[WeaponInstance] = None
