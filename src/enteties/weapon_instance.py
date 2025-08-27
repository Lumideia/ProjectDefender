from abc import ABC
from dataclasses import dataclass, field

from src.rules.weapons.weapon import Weapon, ThrowingWeapon, MeleeWeapon, FirearmWeapon

@dataclass
class WeaponInstance(ABC):
    weapon: Weapon


@dataclass
class ThrowingWeaponInstance(WeaponInstance):
    weapon: ThrowingWeapon
    count: int = field(default=0)

    def __post_init__(self) -> None:
        self.count = self.weapon.base_count

    def throw(self) -> bool:
        if self.count >= 0:
            return True
        return False


@dataclass
class FireArmWeaponInstance(WeaponInstance):
    weapon: FirearmWeapon
    current_ammo: int = field(init=False)

    def __post_init__(self) -> None:
        self.current_ammo = self.weapon.mag_size

    def shoot(self) -> bool:
        if self.current_ammo > 0:
            self.current_ammo -= 1
            return True
        return False

    def reload(self):
        self.current_ammo = self.weapon.mag_size
