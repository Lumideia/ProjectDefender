# perks_generated.py
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from src.rules.events.types import EventCtx
from src.rules.perks.perk import PassiveOneTimePerk, PassiveTriggeredPerk, ActivePerk, AuraPerk
from src.rules.perks.registry import register_perk

if TYPE_CHECKING:
    from src.enteties.character_instance import CharacterInstance

@dataclass
@register_perk(1)
class GrenadeTraining(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(2)
class DemolitionBag(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(3)
class HighQualityExplosives(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(4)
class HeavyArtillery(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(5)
class CoverBag(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(6)
class Unshakable(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(7)
class PowerfulDetonator(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(8)
class DenseSmoke(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(9)
class MiniGrenades(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(10)
class BigBoom(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(11)
class TandemWarheads(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(12)
class ArmorPiercer(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(13)
class Trap(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(14)
class EnhancedSuppression(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(15)
class HarassingFire(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(16)
class OppressiveSuppression(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(17)
class Jetpack(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(18)
class FuelEconomy(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(19)
class HardToHit(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(20)
class ReplaceableFuelTank(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(21)
class ConcreteBreaker(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(22)
class HeavyFlyer(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(23)
class WeightyArgument(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(24)
class Lethality(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(25)
class DualWielding(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(26)
class PistolMaster(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(27)
class CombatHardened(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(28)
class TimeToKill(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(29)
class GoodPreparation(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(30)
class PointBlankShot(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(31)
class LargeCaliber(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(32)
class ExtendedStocks(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(33)
class LowSilhouette(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(34)
class LowVisibility(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(35)
class DeadOnTarget(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(36)
class KnifeThrow(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(37)
class QuickThrow(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(38)
class StrikeFromShadow(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(39)
class Cutthroat(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(40)
class SilentKiller(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(41)
class LightBandaging(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(42)
class BactaReserve(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(43)
class HighQualityBacta(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(44)
class Smoker(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(45)
class FieldMedic(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(46)
class BactaSpray(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(47)
class TrueSavior(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(48)
class PistolMasterPlus(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(49)
class Unyielding(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(50)
class LethalDamage(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(51)
class TraumaticGrenades(PassiveTriggeredPerk):
    cooldown: int = 0
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(52)
class DisruptionGrenades(PassiveTriggeredPerk):
    cooldown: int = 0
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(53)
class FullReadinessGrenade(PassiveTriggeredPerk):
    cooldown: int = 0
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(54)
class Ignition(PassiveTriggeredPerk):
    cooldown: int = 0
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(86)
class AntiPersonnelMine(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(87)
class PowerfulThrow(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(88)
class RapidDeployment(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(89)
class WhatToDetonate(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(90)
class CreateGrenade(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True




@dataclass
@register_perk(100)
class AntiPersonnelMine(ActivePerk):
    cooldown: int = 2
    usage_count: Optional[int] = None
    def on_activate(self, actor, *args, **kwargs): ...









@dataclass
@register_perk(156)
class Aggression(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(157)
class MeleeMaster(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...
