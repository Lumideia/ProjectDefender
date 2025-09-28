from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, TYPE_CHECKING, Type

from src.rules.events.types import EventCtx, Event
from src.enteties.weapon_instance import FireArmWeaponInstance

if TYPE_CHECKING:

    from src.enteties.character_instance import CharacterInstance, ForceUser
    from src.rules.characters.operative import Operative

@dataclass
class Perk(ABC):
    owner: "CharacterInstance" = field(default=None, init=False, repr=False)
    cooldown: int = 0
    is_activated: bool = False
    is_active: bool = False
    is_amendable: bool = False
    available_classes: List["Operative"] = field(default_factory=list)
    usage_area: int = 0
    perks_required: List[Type['Perk']] = field(default_factory=list)
    cd_left: int = field(default=0, init=False, repr=False)
    is_taken: Optional[bool] = None
    is_main_perk: bool = True
    usage_count: int = None
    on_gain_used: bool = field(default=False, init=False)
    is_completed: bool = False # TODO: Change after implementing all perks

    @property
    def id(self) -> int:
        return self.__class__.perk_id
    
    def tick(self) -> None:
        if self.cd_left > 0:
            self.cd_left -= 1
    
    def start_cooldown(self) -> None:
        self.cd_left = self.cooldown
        
    def could_be_activated(
            self, actor: "CharacterInstance", target: Optional["CharacterInstance"] = None, *args, **kwargs
    ) -> bool:
        return True

    def on_gain(self, actor: "CharacterInstance") -> None:
        if self.on_gain_used:
            return
        self.apply_once(actor)
        self.on_gain_used = True

    def apply_once(self, actor: "CharacterInstance") -> None:
        pass

    def consume_use(self) -> None:
        if self.uses_left is not None and self.uses_left > 0:
            self.uses_left -= 1

    def events(self) -> Tuple[Event, ...]:
        return ()

    def __post_init__(self) -> None:
        self.uses_left = self.usage_count



@dataclass
class PassiveOneTimePerk(Perk):
    """Perk which works only once to grant some special improvements"""
    is_activated: bool = field(default=False, init=False)


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
        if not self.is_taken:
            return False
        if self.cd_left > 0:
            return False
        if self.uses_left is not None and self.uses_left == 0:
            return False
        if self.used_on_current_turn:
            return False
        return True

    def could_be_activated(self, actor: "CharacterInstance", target: Optional["CharacterInstance"] = None, *args, **kwargs):
        if not self.ready():
            return False
        return super().could_be_activated(actor, target, *args, **kwargs)

    def try_trigger(self, actor: "CharacterInstance", ctx: Optional[EventCtx] = None, *args, **kwargs) -> bool:
        if not self.ready():
            return False
        if not self.conditions_met(actor, ctx):
            return False
        self.consume_use()
        self.apply_effect(actor, ctx)

        self.start_cooldown()
        if self.used_on_current_turn is not None:
            self.used_on_current_turn = True

        return True

    @abstractmethod
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        pass

    @abstractmethod
    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
class ActivePerk(Perk):
    is_ends_turn: bool = False
    is_activated: bool = field(default=True, init=False)

    def ready(self) -> bool:
        if not self.is_taken:
            return False
        if not self.is_activated:
            return False
        if self.cd_left > 0:
            return False
        if self.uses_left is not None and self.uses_left <= 0:
            return False
        return True


    def could_be_activated(self, actor: "CharacterInstance", target: Optional["CharacterInstance"] = None, *args, **kwargs):
        if not self.ready():
            return False
        return super().could_be_activated(actor, target, *args, **kwargs)

    def try_trigger(self, actor: "CharacterInstance", *args, **kwargs) -> bool:
        if not self.on_activate(actor, *args, **kwargs):
            return False
        self.consume_use()
        self.start_cooldown()
        return True

    @abstractmethod
    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True


@dataclass
class BulletSpendingPerk(ActivePerk):
    ammo_using: int = 0
    use_main_weapon: bool = True

    def could_be_activated(  # TODO rewrite to ready
            self, actor: "CharacterInstance", target: Optional["CharacterInstance"] = None, *args, **kwargs
    ) -> bool:
        weapon = actor.main_weapon if self.use_main_weapon else actor.side_weapon
        if self.ammo_using and isinstance(weapon, FireArmWeaponInstance):
            if weapon.current_ammo < self.ammo_using:
                return False
        return super().could_be_activated(actor, *args, **kwargs)

    def use_ammo(self, actor: "CharacterInstance", bullets):
        weapon = actor.main_weapon if self.use_main_weapon else actor.side_weapon
        if not isinstance(weapon, FireArmWeaponInstance):
            raise Exception('Wrong weapon type')

        weapon.shoot(bullets=bullets)


    def try_trigger(self, actor: "CharacterInstance", *args, **kwargs) -> bool:
        if super().try_trigger(actor, *args, **kwargs):
            self.use_ammo(actor, kwargs.get('ammo_using', self.ammo_using))


    @abstractmethod
    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

class SpecialSpendingPerk(ActivePerk): # TODO: Review if it needs to be generalized
    consumable_using: int = 0
    use_main_weapon = True

    def could_be_activated(
            self, actor: "CharacterInstance", target: Optional["CharacterInstance"] = None, *args, **kwargs
    ) -> bool:
        if actor.consumable_count < self.consumable_using:
            return False
        return super().could_be_activated(actor, *args, **kwargs)

    def on_activate(self, actor, *args, **kwargs) -> bool:
        actor.consumable_count -= self.consumable_using
        ...
        return True


@dataclass
class AuraPerk(Perk):
    is_activated: bool = field(default=False, init=False)
    activation_distance: int = 20

    def events(self) -> Tuple[Event, ...]:
        return Event.PRE_ATTACK, Event.PRE_DEFENSE

    def try_trigger(self, owner: "CharacterInstance", ctx: EventCtx) -> bool:
        return self.apply_to_ctx(owner, ctx)

    @abstractmethod
    def apply_to_ctx(self, owner: "CharacterInstance", ctx: EventCtx) -> bool:
        pass


@dataclass
class ForceActivePerk(ActivePerk):
    owner: "ForceUser" = field(default=None, init=False, repr=False)
    use_force_points: Optional[int] = 0
    could_be_use_as_inertia: bool = False

    def force_use(self, amount: int = None) -> None:
        to_use = amount if amount is not None else self.use_force_points
        if self.owner.force_points >= to_use:
            self.owner.force_points -= to_use

    def ready(self) -> bool:
        if self.owner.inertia and not self.could_be_use_as_inertia:
            return False
        if self.use_force_points is not None and self.owner.force_points < self.use_force_points:
            return False
        return super().ready()

    def try_trigger(self, actor: "ForceUser", *args, **kwargs) -> bool:
        if super().try_trigger(actor, *args, **kwargs):
            self.force_use(kwargs.get('use_force_points', self.use_force_points))
            return True
        return False

    @abstractmethod
    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True


@dataclass
class ForcePassiveTriggeredPerk(PassiveTriggeredPerk):
    owner: "ForceUser" = field(default=None, init=False, repr=False)
    use_force_points: Optional[int] = 0

    def force_use(self, amount: int = None) -> None:
        to_use = amount if amount is not None else self.use_force_points
        if self.owner.force_points >= to_use:
            self.owner.force_points -= to_use

    def ready(self) -> bool:
        if self.use_force_points is not None and self.owner.force_points < self.use_force_points:
            return False
        return super().ready()

    def try_trigger(self, actor: "CharacterInstance", ctx: Optional[EventCtx] = None, *args, **kwargs) -> bool:
        if super().try_trigger(actor, ctx, *args, **kwargs):
            self.force_use(kwargs.get('use_force_points', self.use_force_points))
            return True
        return False

    @abstractmethod
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        pass

    @abstractmethod
    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
class AdditionalPerk:
    is_main_perk: bool = False
    points_cost: int = 0
    is_jedi_perk: bool = False

@dataclass
class AdditionalJediPerk(AdditionalPerk):
    is_jedi_perk: bool = field(default=True)

