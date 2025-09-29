from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional

from src.rules.dice import Dice
from src.rules.weapons.modifiers import DistanceModifier



@dataclass
class Weapon(ABC):
    name: str = ''
    base_dices: List[Dice] = None
    cr_dices: List[Dice] = None
    bonus_dices: [List[Dice]] = None
    movement_effects: int = 0
    armor_ignorance: int = 0
    armor_destroying: int = 0
    is_move_attack_allowed: bool = False
    base_atk: int = 0
    base_acc: int = 85
    base_cr: int = 0

    distance_rules: Optional[List[DistanceModifier]] = None
    def post__init__(self):
        self.distance_rules = sorted(
            self.distance_rules,
            key=lambda r: r.min_distance,
            reverse=True
        ) if self.distance_rules else None


@dataclass
class FirearmWeapon(Weapon):
    mag_size: int = 20
    reload_cost: int = 1
    is_heavy: bool = False
    is_stun_mode_available: bool = False

@dataclass
class MachineGun(FirearmWeapon):
    is_heavy: bool = True
    is_stun_mode_available: bool = True
    critical_armor_destroying: Optional[List[Dice]] = field(default_factory=list)

@dataclass
class ThrowingWeapon(Weapon):
    max_distance: int = 30
    base_count: int = 0

@dataclass
class MeleeWeapon(Weapon):
    base_acc: int = 100
    distance_rules: Optional[List[DistanceModifier]] = None