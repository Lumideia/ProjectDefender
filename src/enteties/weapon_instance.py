from abc import ABC
from dataclasses import dataclass, field

from src.rules.weapons.weapon import Weapon, ThrowingWeapon, MeleeWeapon, FirearmWeapon

@dataclass
class WeaponInstance(ABC):
    current_ammo: int = field(init=False, default=0)
    weapon: Weapon


@dataclass
class ThrowingWeaponInstance(WeaponInstance):
    weapon: ThrowingWeapon
    count: int = field(default=0)

    def __post_init__(self) -> None:
        self.count = self.weapon.base_count

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
