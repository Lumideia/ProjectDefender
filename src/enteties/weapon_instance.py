from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional

from src.rules.dice import Dice
from src.rules.weapons.modifiers import DistanceModifier
from src.rules.weapons.weapon import Weapon, ThrowingWeapon, MeleeWeapon, FirearmWeapon

@dataclass
class WeaponInstance(ABC):
    base_acc: int = field(init=False)
    current_ammo: int = field(init=False, default=0)
    weapon: Weapon
    base_dices = List[Dice]
    cr_dices = List[Dice]
    movement_effects: int = field(init=False)
    armor_destroying: int = field(init=False)
    is_move_attack_allowed: bool = field(init=False)
    base_atk: int = field(init=False)
    base_cr: int = field(init=False)
    bonus_dices: Optional[List[Dice]] = field(default=None)

    def __post_init__(self):
        self.name = self.weapon.name
        self.base_dices = self.weapon.base_dices
        self.cr_dices = self.weapon.cr_dices
        self.movement_effects = self.weapon.movement_effects
        self.armor_destroying = self.weapon.armor_destroying
        self.is_move_attack_allowed = self.weapon.is_move_attack_allowed
        self.base_atk = self.weapon.base_atk
        self.base_acc = self.weapon.base_acc
        self.base_cr = self.weapon.base_cr
        self.bonus_dices = self.weapon.bonus_dices


@dataclass
class ThrowingWeaponInstance(WeaponInstance):
    weapon: ThrowingWeapon
    count: int = field(default=0)

    def __post_init__(self) -> None:
        self.count = self.weapon.base_count
        super().__post_init__()

    def throw(self) -> bool:
        if self.count > 0:
            self.count -= 1
            return True
        return False

    def pick_up(self) -> bool:
        self.count += 1
        return True


@dataclass
class FireArmWeaponInstance(WeaponInstance):
    weapon: FirearmWeapon
    current_ammo: int = field(init=False)

    def __post_init__(self) -> None:
        self.current_ammo = self.weapon.mag_size
        super().__post_init__()

    def shoot(self, bullets=1) -> bool:
        if self.current_ammo > 0:
            self.current_ammo -= bullets
            return True
        return False

    def reload(self):
        self.current_ammo = self.weapon.mag_size

    def load_bullets(self, count=1) -> bool:
        if self.current_ammo + count <= self.weapon.mag_size:
            self.current_ammo += count
            return True
        return False


@dataclass
class MeleeWeaponInstance(WeaponInstance):
    weapon: MeleeWeapon


def create_weapon_instance(weapon: Weapon) -> WeaponInstance:
    if isinstance(weapon, FirearmWeapon):
        return FireArmWeaponInstance(weapon=weapon)
    elif isinstance(weapon, ThrowingWeapon):
        return ThrowingWeaponInstance(weapon=weapon)
    elif isinstance(weapon, MeleeWeapon):
        return MeleeWeaponInstance(weapon=weapon)
