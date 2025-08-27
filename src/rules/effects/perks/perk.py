from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from src.enteties.weapon_instance import FireArmWeaponInstance
from src.rules.characters.operative import Operative, Character
from src.rules.effects.effect import Effect


@dataclass
class Perk(ABC):
    cooldown: int = 0
    is_activated: bool = True
    is_active: bool = False
    is_amendable: bool = False
    available_classes: List['Operative'] = field(default_factory=list)
    usage_area: int = 0
    perks_required: List['Perk'] = field(default_factory=list)



@dataclass
class ActivePerk(Perk):
    is_ends_turn: bool = False
    is_active: bool = field(default=True, init=False)
    cd_left: int = field(default=0, init=False, repr=False)
    usage_count: int = None

    def __post_init__(self) -> None:
        self.uses_left = self.usage_count

    @property
    def ready(self) -> bool:
        if not self.is_activated:
            return False
        if self.cd_left > 0:
            return False
        if self.uses_left is not None and self.uses_left <= 0:
            return False
        return True

    def tick(self) -> None:
        if self.cd_left > 0:
            self.cd_left -= 1

    def start_cooldown(self) -> None:
        self.cd_left = self.cooldown

    def consume_use(self) -> None:
        if self.uses_left is not None and self.uses_left > 0:
            self.uses_left -= 1

    def activate(self, actor: Operative, *args, **kwargs) -> bool:
        if not self.ready:
            return False
        if not self.on_activate(actor, *args, **kwargs):
            return False
        self.consume_use()
        self.start_cooldown()
        return True

    @abstractmethod
    def on_activate(self, actor, *args, **kwargs) -> bool:
        raise NotImplementedError


@dataclass
class AttackPerk(ActivePerk):
    ammo_using: int = 0
    use_main_weapon = True

    def activate(self, actor: Operative, *args, **kwargs) -> bool:
        weapon = actor.main_weapon if self.use_main_weapon else actor.side_weapon
        if self.ammo_using and isinstance(weapon, FireArmWeaponInstance):
            if weapon.current_ammo < self.ammo_using:
                return False
        return super().activate(actor, *args, **kwargs)



@dataclass
class EffectPerk(Perk):
    targets: List['Character'] = field(default_factory=list)
    effects: List['Effect'] = field(default_factory=list)

    @abstractmethod
    def on_activate(self, actor, *args, **kwargs) -> bool:
        raise NotImplementedError
