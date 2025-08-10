from abc import ABC
from typing import List

from src.rules.characters.operative import Operative


class Perk(ABC):
    cooldown: int = 0
    is_activated: bool = True
    is_active: bool = False
    is_amendable: bool = False
    available_classes: List[Operative] = None
    ammo_using: int = 0
    is_ends_turn: bool = False
    usage_area: int = 0
    perks_required: list
    usage_count: int = None

class FlyingManPerk(Perk):
    fuel_consumption: int
