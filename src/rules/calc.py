from dataclasses import dataclass, field
from typing import Optional

from src.enteties.weapon_instance import WeaponInstance
from src.rules.characters.character import Character
from src.rules.weapons.weapon import Weapon
from src.rules.weapons.cover import Position, Cover, Interference


class FutureCalculation:
    """Should be used in future versions"""

    def __init__(self, attack: Character = None, weapon: Weapon = None, defense: Character = None, distance: int = 0):
        self.attack = attack
        self.weapon = weapon
        self.defense = defense
        self.distance = distance
        self.distance_rule = None
        if hasattr(weapon, 'distance_rules'):
            self.distance_rule = weapon.get_distance_rule(distance)

    def calculate_accuracy(self):
        base_acc = self.attack.accuracy - self.defense.accuracy
        if self.distance_rule.accuracy_abs:
            return base_acc + self.distance_rule.accuracy_buff
        return base_acc * self.distance_rule.accuracy_buff

    def calculate_cr(self):
        return self.attack.cr - self.defense.cr + self.distance_rule.cr_buff


@dataclass
class LegacyCalculation:
    weapon: Optional["WeaponInstance"] = None
    distance: int = 0
    relative_position: Position = Position.EQUAL
    cover: Cover = field(default_factory=Cover)
    interference: Interference = field(default_factory=Interference)

    base_acc: int = field(default=85, init=False)
    base_cr: int = field(default=0, init=False)

    distance_damage_mult: float = field(default=1.0, init=False)
    distance_acc: int = field(default=0, init=False)
    distance_cr: int = field(default=0, init=False)

    ignore_small_interference: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.base_acc = self.weapon.base_acc
        self.base_cr = self.weapon.base_cr
        if self.relative_position == Position.LOWER:
            self.base_acc -= 15
            self.base_cr -= 5
        elif self.relative_position == Position.HIGHER:
            self.base_acc += 15
            self.base_cr += 5
            self.ignore_small_interference = True

        if self.weapon.weapon.distance_rules:
            rule = self.weapon.weapon.get_distance_rule(self.distance)
            self.distance_damage_mult, self.distance_acc, self.distance_cr = rule.calculate_penalties(self.distance)
        else:
            self.distance_damage_mult, self.distance_acc, self.distance_cr = 1.0, 0, 0

    def calculate_accuracy(self) -> int:
        cover_acc_penalty = self.cover.total_penalty()
        interference_acc_penalty = self.interference.total_penalty(
            only_full=self.ignore_small_interference
        )
        return self.base_acc + self.distance_acc - cover_acc_penalty - interference_acc_penalty

    def calculate_cr(self) -> int:
        return self.base_cr + self.distance_cr

    def calculate_dmg_buff(self) -> float:
        return self.distance_damage_mult
