from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from src.enteties.weapon_instance import FireArmWeaponInstance
from src.enteties.character_instance import CharacterInstance
from src.rules.characters.operative import Operative
from src.rules.effects.effect import Effect
from src.rules.events.types import EventCtx


@dataclass
class Perk(ABC):
    owner: CharacterInstance = field(default=None, init=False, repr=False)
    cooldown: int = 0
    is_activated: bool = True
    is_active: bool = False
    is_amendable: bool = False
    available_classes: List['Operative'] = field(default_factory=list)
    usage_area: int = 0
    perks_required: List['Perk'] = field(default_factory=list)
    cd_left: int = field(default=0, init=False, repr=False)
    
    def tick(self) -> None:
        if self.cd_left > 0:
            self.cd_left -= 1
    
    def start_cooldown(self) -> None:
        self.cd_left = self.cooldown
        
    def could_be_activated(
            self, actor: CharacterInstance, target: Optional[CharacterInstance] = None, *args, **kwargs
    ) -> bool:
        return True

    def on_gain(self, actor: CharacterInstance) -> bool:
        pass



@dataclass
class PassiveOneTimePerk(Perk):
    """Perk which works only once to grant some special improvements"""
    used: bool = field(default=False, init=False)

    def on_gain(self, actor: CharacterInstance) -> None:
        if self.used:
            return
        self.apply_once(actor)
        self.used = True

    @abstractmethod
    def apply_once(self, actor: CharacterInstance) -> None:
        pass

@dataclass
class PassiveTriggeredPerk(Perk):
    """Passive perks with activation conditions"""
    used_on_current_turn: bool = field(default=None, repr=False)

    def tick(self) -> None:
        if self.cd_left > 0:
            self.cd_left -= 1
        if self.used_on_current_turn is not None:
            self.used_on_current_turn = False

    def ready(self) -> bool:
        if self.cd_left > 0:
            return False
        if self.used_on_current_turn:
            return False
        return True

    def try_trigger(self, actor: CharacterInstance, ctx: Optional[EventCtx] = None) -> bool:
        if not self.ready():
            return False
        if not self.conditions_met(actor, ctx):
            return False
        self.apply_effect(actor, ctx)

        self.start_cooldown()
        if self.used_on_current_turn is not None:
            self.used_on_current_turn = True

        return True

    @abstractmethod
    def conditions_met(self, actor: CharacterInstance, ctx: Optional[EventCtx]) -> bool:
        pass

    @abstractmethod
    def apply_effect(self, actor: CharacterInstance, ctx: Optional[EventCtx]) -> None:
        pass

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

    def consume_use(self) -> None:
        if self.uses_left is not None and self.uses_left > 0:
            self.uses_left -= 1

    def could_be_activated(self, actor: CharacterInstance, target: Optional[CharacterInstance] = None, *args, **kwargs):
        if not self.ready:
            return False
        return self.could_be_activated(actor, target, *args, **kwargs)

    def activate(self, actor: Operative, *args, **kwargs) -> bool:
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

    def could_be_activated(
            self, actor: CharacterInstance, target: Optional[CharacterInstance] = None, *args, **kwargs
    ) -> bool:
        weapon = actor.main_weapon if self.use_main_weapon else actor.side_weapon
        if self.ammo_using and isinstance(weapon, FireArmWeaponInstance):
            if weapon.current_ammo < self.ammo_using:
                return False
        return super().could_be_activated(actor, *args, **kwargs)


@dataclass
class TargetedPerk(ActivePerk):
    def could_be_activated(
            self, actor: CharacterInstance, target: Optional[CharacterInstance] = None, *args, **kwargs
    ) -> bool:
        return super().could_be_activated(actor, target, *args, **kwargs)


@dataclass
class DefensivePerk(Perk):
    pass


@dataclass
class AuraEffectPerk(Perk):
    activation_distance: int = 20

    def remove_effect(self, target: CharacterInstance) -> None:
        pass

    def within_radius(self, target: CharacterInstance) -> bool:
        dx, dy = target.x - self.owner.x, target.y - self.owner.y
        return (dx * dx + dy * dy) ** 0.5 <= self.activation_distance

    def is_valid_target(self, target: CharacterInstance) -> bool:
        pass

    def refresh_state(self, target: CharacterInstance) -> None:
        if self.owner.hp <= 0:  # TODO: review product logic of death
            self.remove_effect(target)
            return
        if not self.is_valid_target(target):
            self.remove_effect(target)
            return
        if not self.within_radius(target):
            self.remove_effect(target)
            return


    def try_trigger(self, actor: CharacterInstance, ctx: Optional[EventCtx] = None) -> bool:
        if not self.ready():
            return False
        if not self.conditions_met(actor, ctx):
            return False
        self.apply_effect(actor, ctx)

        self.start_cooldown()
        if self.used_on_current_turn is not None:
            self.used_on_current_turn = True

        return True

    @abstractmethod
    def conditions_met(self, actor: CharacterInstance, ctx: Optional[EventCtx]) -> bool:
        pass

    @abstractmethod
    def apply_effect(self, actor: CharacterInstance, ctx: Optional[EventCtx]) -> None:
        pass
