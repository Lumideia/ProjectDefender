from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional, Union

from src.rules.dice import Dice, format_dice
from src.rules.weapons.modifiers import DistanceModifier
from src.rules.weapons.weapon import Weapon, ThrowingWeapon, MeleeWeapon, FirearmWeapon, MachineGun


@dataclass
class WeaponInstance(ABC):
    base_acc: int = field(init=False)
    current_ammo: int = field(init=False)
    weapon: Weapon
    base_dices: List[Dice] = field(init=False)
    cr_dices: List[Dice] = field(init=False)
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

    def additional_info(self) -> List[str]:
        return []


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


class MachineGunWeaponInstance(FireArmWeaponInstance):
    weapon: MachineGun

    def __post_init__(self) -> None:
        super().__post_init__()
        self.critical_armor_destroying = self.weapon.critical_armor_destroying

    def additional_info(self) -> List[str]:
        if self.critical_armor_destroying:
            return [f"Разрыв брони при крите: {format_dice(self.critical_armor_destroying)}"]
        return []

def create_weapon_instance(weapon: Weapon) -> Union[
    MeleeWeaponInstance, FireArmWeaponInstance, ThrowingWeaponInstance, None
]:
    if isinstance(weapon, FirearmWeapon):
        if isinstance(weapon, MachineGun):
            return MachineGunWeaponInstance(weapon=weapon)
        return FireArmWeaponInstance(weapon=weapon)
    elif isinstance(weapon, ThrowingWeapon):
        return ThrowingWeaponInstance(weapon=weapon)
    elif isinstance(weapon, MeleeWeapon):
        return MeleeWeaponInstance(weapon=weapon)
    return None
