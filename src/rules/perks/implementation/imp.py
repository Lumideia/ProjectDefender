# perks_generated.py
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING, List

from src.rules.consumables.InventoryCell import GrenadeOnlyCell, TypedInventoryCell
from src.rules.consumables.consumable import Smoke, Grenade, ThermalDetonator, Flashing, BaktaSpray, EnergeticWeb, \
    EMIGrenade, GasGrenade, ImpulseGrenade, Cryogen, DamageGrenade, NonDamageGrenade, Bandage
from src.rules.dice import Dice
from src.rules.events.types import EventCtx
from src.rules.perks.perk import (
    PassiveOneTimePerk, PassiveTriggeredPerk, ActivePerk, AuraPerk, AdditionalPerk, AdditionalJediPerk, ForceActivePerk,
    ForcePassiveTriggeredPerk
)
from src.rules.perks.registry import register_perk

if TYPE_CHECKING:
    from src.enteties.character_instance import CharacterInstance, ForceUser, ElectricGuard


@dataclass
@register_perk(1)
class GrenadeTraining(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(2) # TODO: Not completed, test
class DemolitionBag(PassiveOneTimePerk):
    def apply_once(self, actor):
        for _ in range(7):
            actor.inventory.add_cell(GrenadeOnlyCell())
        self.is_completed = True


@dataclass
@register_perk(3)
class HighQualityExplosives(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(4)
class HeavyArtillery(PassiveOneTimePerk):
    def apply_once(self, actor):
        actor.inventory.add_cell(TypedInventoryCell(available_consumables=[DamageGrenade]))
        actor.inventory.add_cell(TypedInventoryCell(available_consumables=[DamageGrenade]))
        self.is_completed = True

@dataclass
@register_perk(5)
class CoverBag(PassiveOneTimePerk):
    def apply_once(self, actor):
        actor.inventory.add_cell(TypedInventoryCell(available_consumables=[NonDamageGrenade]))
        actor.inventory.add_cell(TypedInventoryCell(available_consumables=[NonDamageGrenade]))
        self.is_completed = True

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
    def apply_once(self, actor):
        DemolitionBag().apply_once(actor)

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
    def apply_once(self, actor):
        actor.main_weapon.base_dices.extend([Dice(6), Dice(6)])
        self.is_completed = True

@dataclass
@register_perk(25)
class DualWielding(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(26)
class PistolMaster(PassiveOneTimePerk):
    def apply_once(self, actor):
        actor.main_weapon.base_dices = [Dice(10)]
        self.is_completed = True

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
    def apply_once(self, actor):
        actor.mobility = 40
        self.is_completed = True

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
    def apply_once(self, actor):
        actor.main_weapon.base_dices.extend([Dice(4), Dice(4), Dice(4)])
        self.is_completed = True

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
    def apply_once(self, actor):
        actor.available_consumables.append(Bandage)
        for _ in range(10):
            cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[Bandage]))
            actor.inventory.add_to_specific_cell(cell, Bandage())
        self.is_completed = True

@dataclass
@register_perk(42)
class BactaReserve(PassiveOneTimePerk):
    def apply_once(self, actor):
        for _ in range(3):
            cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[BaktaSpray]))
            actor.inventory.add_to_specific_cell(cell, BaktaSpray())
        self.is_completed = True

@dataclass
@register_perk(43)
class HighQualityBacta(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(44)
class Smoker(PassiveOneTimePerk):
    def apply_once(self, actor):
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[Smoke]))
        actor.inventory.add_to_specific_cell(cell, Smoke())
        self.is_completed = True

@dataclass
@register_perk(45)
class FieldMedic(PassiveOneTimePerk):
    def apply_once(self, actor):
        BactaReserve().apply_once(actor)
        self.is_completed = True

@dataclass
@register_perk(46)
class BaktaSpraying(PassiveOneTimePerk):
    def apply_once(self, actor):
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[Smoke]))
        actor.inventory.add_to_specific_cell(cell, Smoke())
        self.is_completed = True

@dataclass
@register_perk(47)
class TrueSavior(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(48)
class PistolMasterPlus(PassiveOneTimePerk):
    def apply_once(self, actor):
        actor.main_weapon.base_dices.append(Dice(4))
        self.is_completed = True

@dataclass
@register_perk(49)
class Unyielding(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(50)
class LethalDamage(PassiveOneTimePerk):
    def apply_once(self, actor):
        actor.main_weapon.base_dices = [Dice(4), Dice(4), Dice(4)]
        self.is_completed = True

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
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(55)
class HolographicAiming(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(56)
class FullReadinessShot(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(57)
class Chaos(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(58)
class Invulnerability(PassiveTriggeredPerk): # TODO: MADE ACTIVE STATE UNTIL CANCEL
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(59) # TODO: PROGESSION EFFECT
class LightningReaction(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(60)
class DeathFromAbove(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(61)
class HitAndRun(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(62)
class SkyDebut(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(63)
class CombatAwareness(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 3
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(64)
class OnEdge(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(65)
class CircularReload(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(66)
class ElectricSpikes(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(67)
class ShootersKata(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(68)
class Checkmate(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(69)
class HitAndRunEx(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(70)
class ReflectiveReload(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(71)
class FaceToFace(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(72)
class Reflexes(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(73)
class KingOfBattle(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(74)
class LickingWounds(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(75)
class CloseContacts(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(76)
class ReturnFire(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(77)
class Debut(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(78)
class SightingIn(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(79)
class AlwaysOnGuard(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(80)
class Hunter(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(81)
class SituationControl(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(82)
class Brutality(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(83)
class GoodReaction(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(84)
class CollectTheFragments(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(85)
class Sentinel(PassiveTriggeredPerk):
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
@register_perk(89) # TODO: Weapon
class WhatToDetonate(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(90) # TODO: Consume
class CreateGrenade(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True


@dataclass
@register_perk(91) # TODO: Weapon
class Suppression(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True


@dataclass
@register_perk(92) # TODO: Weapon
class WideSuppression(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(93) # TODO: Upgrade
class DangerZone(PassiveOneTimePerk):
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(94) # TODO: Weapon
class ChainWeight(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(95) # TODO: Weapon
class Rupture(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(96) # TODO: Weapon
class RapidFire(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(97) # TODO: Weapon
class TripleShot(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(98) # TODO: Weapon
class SurefireShot(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(99) # TODO: Weapon
class MassiveFire(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True


@dataclass
@register_perk(100) # TODO: Weapon
class KillChain(ActivePerk):
    cooldown: int = 4

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(101)
class KillZone(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(102) # TODO: Consume
class JetLeap(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(103) # TODO: Consume, Ground state
class Hover(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(104) # TODO: Consume, Ground state
class SkyShot(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(105) # TODO: Consume, size condition
class GroundSlam(ActivePerk): # TODO: Consume
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(106) # TODO: Jopa
class AlternativeFuelSource(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 3

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(107) #TODO: PERK REQUIRED
class HomingMissile(ActivePerk):
    cooldown: int = 1
    perks_required: list = field(default_factory=lambda: [ConcreteBreaker])

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(108) # TODO: Consume, Ground state
class DeathRay(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(109)
class CommandOrder(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(110)
class PistolStrike(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(111)
class MarkTarget(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(112)
class LegShot(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(113)
class Bombard(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(114)
class TakeThis(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(115)
class MoveOut(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(116) # TODO: Weapon
class PistolBarrage(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(117)
class BeyondLimits(ActivePerk):
    cooldown: int = 7

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(118)
class ConcentratedFire(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(119)
class RunAndGun(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(120)
class ReloadOnTheRun(PassiveOneTimePerk):
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...


@dataclass
@register_perk(121)
class Preparation(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(122)
class Dash(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(123)
class Fortify(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(124) # TODO: Weapon
class StreetSweeper(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(125) # TODO: Weapon 1
class FanShot(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(126) # TODO: Weapon
class LightningHands(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(127) # TODO: Weapon
class QuickHands(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(128) # TODO: Weapon
class Bullseye(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(129) # TODO: Weapon
class BulletStorm(ActivePerk):
    cooldown: int = 5

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(130)
class PerfectAim(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(131)
class SituationalAwareness(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(132)
class PreciseShot(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(133)  #TODO: CONSUMABLE
class ExplosiveShot(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(134) # TODO: Weapon
class EMPBlast(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(135)
class FasterThanThought(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(136)
class RicochetShot(ActivePerk):
    cooldown: int = 0
    usage_count = 5

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(137) # TODO: Weapon
class DoubleTap(ActivePerk):
    cooldown: int = 4

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(138)
class StepIntoShadow(ActivePerk):
    cooldown: int = 4

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(139)
class Jammer(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(140)
class KnifeTrick(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(141)
class BerserkStrike(ActivePerk):
    cooldown: int = 5

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(142)
class Scanning(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(143)
class QuickScanner(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True


@dataclass
@register_perk(144)
class FindWeakness(PassiveOneTimePerk):
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...


@dataclass
@register_perk(145)
class Igniter(PassiveOneTimePerk):
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...


@dataclass
@register_perk(146)
class OpticOverload(PassiveOneTimePerk):
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...


@dataclass
@register_perk(147)
class MicroMotorTracking(PassiveOneTimePerk):
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...


@dataclass
@register_perk(148)
class MassScan(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True
    def on_gain(self, actor: "CharacterInstance") -> bool:
        return True


@dataclass
@register_perk(149)
class Stimulate(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(150) # TODO: CONSUME
class Paramedic(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True
    def on_gain(self, actor: "CharacterInstance") -> bool:
        return True

@dataclass
@register_perk(151)
class MedicWithYou(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(152)
class SnapShot(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...


@dataclass
@register_perk(153)
class ShieldTrauma(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(154)
class NotJustHit(PassiveOneTimePerk):
    def apply_once(self, actor: "CharacterInstance") -> None:
        pass

@dataclass
@register_perk(155)
class ShieldCharge(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True




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

@dataclass
@register_perk(158)
class Avenger(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...


@dataclass
@register_perk(159)
class LoneWolf(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...


@dataclass
@register_perk(160)
class ComeOnBringItOn(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(161)
class Elusive(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(162)
class ReliableCover(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(163)
class StrengthInUnity(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(164)
class ShieldWall(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(165)
class MobileCover(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(166)
class SuperGuardian(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(167)
class ImpeccableDefense(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(168)
class Taunt(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(169)
class Absolute(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

    def on_gain(self, actor: "CharacterInstance") -> bool:
        return True

@dataclass
@register_perk(170)
class ChargingPistol(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(171)
class ServeAndProtect(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(172)
class Threat(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(173)
class ExplosionProof(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(174)
class EveryoneOnGuard(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(175)
class EngineerBag(PassiveOneTimePerk):
    def apply_once(self, actor): ...

@dataclass
@register_perk(176) # TODO: CONSUME
class WeaponUpgrade(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(177)
class ItemDelivery(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(178) # TODO: Ally control
class ProtocolSupport(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(179)
class NetworkDive(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(180)
class ItemDrop(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(181) # TODO: CONSUME Ally control
class CombatDroneDeployment(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(182)
class ProtocolAttack(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(183)
class ImprovedStun(PassiveTriggeredPerk):
    is_activated: bool = False
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(184)
class ElectricControl(AuraPerk):
    cooldown: int = 0
    usage_count: Optional[int] = None
    def apply_to_ctx(self, owner, ctx): ...

@dataclass
@register_perk(185)
class TechnicianKit(PassiveOneTimePerk): # TODO: ADD CONSUME
    def apply_once(self, actor): ...

@dataclass
@register_perk(186)
class ProtocolRetreat(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(187)
class FinishingShot(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(188) # TODO: Should change other perk JOPA
class ProtocolChainStrike(PassiveOneTimePerk):
    perks_required: list = field(default_factory=lambda: [ProtocolAttack])
    def apply_once(self, actor): ...

@dataclass
@register_perk(189)
class ProtocolDisappearance(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(190)
class ShieldProjection(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(191) # TODO: ADD CONSUME
class Reprogramming(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(192) # TODO: ADD CONSUME
class ProtocolBastion(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(193) # TODO: ADD CONSUME
class JunkCollector(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(194)
class Repair(ActivePerk):
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(195) # TODO COVER BASED
class WillToLive(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...
 ####


@dataclass
@register_perk(196) # TODO: ADD CONSUME
class Meditation(ActivePerk):
    cooldown: int = 1

    def on_gain(self, actor: "ForceUser") -> None:
        actor.max_force_points += 9
        actor.restore_force_points()

    def on_activate(self, actor, *args, **kwargs):
        actor.restore_force_points()
        return True

@dataclass
@register_perk(197) # TODO: INERTIAL PROPERTY
class Inertia(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        actor.inertia = True

@dataclass
@register_perk(198) # TODO: INERTIAL PROPERTY ADD CONSUME
class LightsaberThrow(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 1
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(199) # TODO: INERTIAL PROPERTY ADD CONSUME
class DefensiveStance(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 1
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(200)  # TODO: INERTIAL PROPERTY ADD CONSUME
class ForceLift(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 1
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(201) # TODO: ADD CONSUME
class ForceBubble(ForcePassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1
    use_force_points: int = 3

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(202) # TODO: ADD CONSUME (WANTED COUNT)
class Ionization(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(203) # TODO: INERTIAL PROPERTY ADD CONSUME
class ForceFlash(ForceActivePerk):
    use_force_points: int = 2
    cooldown: int = 1
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(204) # TODO: INERTIAL PROPERTY ADD CONSUME
class ForcePush(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 2
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(205) # TODO: INERTIAL PROPERTY ADD CONSUME COVER ADD
class ForceBarrier(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 2
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(206) # TODO: INERTIAL PROPERTY ADD CONSUME
class ForceStun(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 1
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(207) # TODO: INERTIAL PROPERTY(!!) ADD CONSUME
class JumpAttack(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 2

    def on_activate(self, actor, *args, **kwargs):
        actor.inertia = True
        return True

@dataclass
@register_perk(208)
class ForceBurst(ForceActivePerk):
    cooldown: int = 1
    perks_required: list = field(default_factory=lambda: [ForcePush])
    use_force_points: int = 4
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(209) # TODO: ADD CONSUME ADD JOPA
class ForcePersuasion(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(210) # TODO: INERTIAL PROPERTY ADD CONSUME ADD ALLY
class ForceProjection(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 4
    could_be_use_as_inertia: bool = True

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(211) # TODO: ADD CONSUME
class ElectricJustice(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(212) # TODO: ADD CONSUME ADD ALLY
class ForceDuplicate(ForceActivePerk):
    cooldown: int = 1
    use_force_points: int = 7

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(213) # TODO: ADD CONSUME
class ForceHeal(ForceActivePerk):
    cooldown: int = 3
    use_force_points: int = 5

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(214)
class ForceSpeed(ForceActivePerk):
    cooldown: int = 3
    use_force_points: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(215) # TODO: Should change other perk
class ReflectionMaster(PassiveOneTimePerk):
    perks_required: list = field(default_factory=lambda: [DefensiveStance])

    def apply_once(self, actor):
        ...


@dataclass
@register_perk(216)
class SharedVision(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(217)
class ArmorPiercer(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(218)
class LongRangeOverwatch(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...


@dataclass
@register_perk(219)
class PreemptiveShot(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(220)
class LightStep(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(221)
class Tracking(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...


@dataclass
@register_perk(222)
class BetweenTheEyes(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...


@dataclass
@register_perk(223)
class LetMeStart(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(224)
class Finisher(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(225) # TODO: Death logic change
class DontDie(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(226)
class SlightMiss(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(227)
class ShieldRegeneration(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(228)
class FightForSurvival(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(229)
class SpecialTechnique(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...

@dataclass
@register_perk(230)
class BackFire(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        ...


@dataclass
@register_perk(231)
class WillToLiveAdditional(AdditionalPerk, WillToLive):
    points_cost: int = 15


@dataclass
@register_perk(232)
class Mist(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5
    def apply_once(self, actor: "CharacterInstance") -> None:
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[Smoke]))
        actor.inventory.add_to_specific_cell(cell, Smoke())
        self.is_completed = True


@dataclass
@register_perk(233)
class Resilience(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 10
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(234)
class Illuminator(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5

    def apply_once(self, actor: "CharacterInstance") -> None:
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[Flashing]))
        actor.inventory.add_to_specific_cell(cell, Flashing())
        self.is_completed = True

@dataclass
@register_perk(235)
class ShoulderBag(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 15
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(236)
class SureAim(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 20
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(237)
class Sprinter(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5
    def apply_once(self, actor: "CharacterInstance") -> None:
        actor.mobility += 5
        self.is_completed = True

@dataclass
@register_perk(238)
class TacticalSense(AdditionalPerk, ActivePerk):
    cooldown: int = 2
    points_cost: int = 15

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(239) # TODO: Think
class TraumaticGrenadesAdditional(AdditionalPerk, TraumaticGrenades):
    points_cost: int = 20
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(240)
class Watcher(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 20
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(241)
class Savior(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 10
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(242)
class SelfSacrifice(AdditionalPerk, ActivePerk):
    points_cost: int = 20
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(243)
class Downpour(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(244)
class ShockWave(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(245)
class LowSilhouetteAdditional(AdditionalPerk, LowSilhouette):
    points_cost: int = 20

@dataclass
@register_perk(246)
class HandyWeapon(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 20
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(247)
class SurefireShotAdditional(AdditionalPerk, SurefireShot):
    is_activated: bool = True
    points_cost: int = 30
    cooldown: int = 3

@dataclass
@register_perk(248)
class Fortification(AdditionalPerk, ActivePerk):
    is_activated: bool = True
    points_cost: int = 15
    cooldown: int = 3

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(249)
class SmokeScreen(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 10
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(250)
class BattleHardened(AdditionalPerk, CombatHardened):
    points_cost: int = 25





@dataclass
@register_perk(251)
class CloseContactsAdditional(AdditionalPerk, CloseContacts):
    points_cost: int = 20


@dataclass
@register_perk(252)
class PainReaction(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(253)
class Bastion(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 10
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(254)
class DashAdditional(AdditionalPerk, Dash):
    is_activated: bool = True
    points_cost: int = 15
    move_bonus: int = 20

@dataclass
@register_perk(255)
class LoneWolfAdditional(AdditionalPerk, LoneWolf):
    points_cost: int = 20
    acc_and_def_bonus: int = 20

@dataclass
@register_perk(256)
class PreciseShotAdditional(AdditionalPerk, PreciseShot):
    is_activated: bool = True
    points_cost: int = 25
    cr_bonus: int = 20

@dataclass
@register_perk(257)
class LickingWoundsAdditional(AdditionalPerk, LickingWounds):
    points_cost: int = 5


@dataclass
@register_perk(258)
class ScoutPerk(AdditionalPerk, ActivePerk):
    points_cost: int = 15
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True

    def on_gain(self, actor: "CharacterInstance") -> bool:
        ...

@dataclass
@register_perk(259)
class BloodRail(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 10

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(260)
class Pharmacist(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5

    def apply_once(self, actor: "CharacterInstance") -> None:
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[BaktaSpray]))
        actor.inventory.add_to_specific_cell(cell, BaktaSpray())
        self.is_completed = True
    
@dataclass
@register_perk(261)
class Immobilizer(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5
    def apply_once(self, actor: "CharacterInstance") -> None:
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[EnergeticWeb]))
        actor.inventory.add_to_specific_cell(cell, EnergeticWeb())
        self.is_completed = True

@dataclass
@register_perk(262)
class MagChange(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 10

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(263)
class Concentration(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(264)
class WarDrugs(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 10
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...


@dataclass
@register_perk(265)
class PreparationAdditional(AdditionalPerk, Preparation):
    points_cost: int = 25


@dataclass
@register_perk(266)
class HitAndRunAdditional(AdditionalPerk, HitAndRun):
    points_cost: int = 20

@dataclass
@register_perk(267)
class InvulnerabilityAdditional(AdditionalPerk, Invulnerability):
    points_cost: int = 30

@dataclass
@register_perk(268)
class RuptureAdditional(AdditionalPerk, Rupture):
    armor_destroying: int = 25
    points_cost: int = 25

@dataclass
@register_perk(269)
class QuickHandsAdditional(AdditionalPerk, QuickHands):
    points_cost: int = 15

@dataclass
@register_perk(270)
class RapidFireAdditional(AdditionalPerk, RapidFire):
    points_cost: int = 30

@dataclass
@register_perk(271)
class CounterShot(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(272)
class Parkour(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 10
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...


@dataclass
@register_perk(273)
class HiddenReserves(AdditionalPerk, ActivePerk):
    points_cost: int = 20
    usage_count: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

    def on_gain(self, actor: "CharacterInstance") -> bool:
        ...

@dataclass
@register_perk(274)
class Unshaken(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 20

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass


@dataclass
@register_perk(275)
class AR(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 15
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(276)
class Predator(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 15
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(277)
class Bullseye(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 15
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(278)
class ThickPadding(AdditionalPerk, ActivePerk):
    points_cost: int = 10

    def on_activate(self, actor, *args, **kwargs):
        return True

    def on_gain(self, actor: "CharacterInstance") -> bool:
        ...

@dataclass
@register_perk(279)
class CoverMe(AdditionalPerk, ActivePerk):
    points_cost: int = 15
    cooldown: int = 2

    def on_activate(self, actor, *args, **kwargs):
        return True

    def on_gain(self, actor: "CharacterInstance") -> bool:
        ...

@dataclass
@register_perk(280)
class BonusExplosive(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5

    def apply_once(self, actor: "CharacterInstance") -> None:
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[ThermalDetonator]))
        actor.inventory.add_to_specific_cell(cell, ThermalDetonator())
        self.is_completed = True

@dataclass
@register_perk(281)
class Jamming(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5

    def apply_once(self, actor: "CharacterInstance") -> None:
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[EMIGrenade]))
        actor.inventory.add_to_specific_cell(cell, EMIGrenade())
        self.is_completed = True

@dataclass
@register_perk(282)
class Kubikiri(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 25

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(283)
class OffensiveStrike(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 10

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(284)
class ArmoredRun(AdditionalPerk, ActivePerk):
    cooldown: int = 2
    points_cost: int = 10

    def on_activate(self, actor, *args, **kwargs) -> bool:
        return True

@dataclass
@register_perk(285)
class CantHide(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(286)
class StationaryThreat(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 25

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(287)
class Assassin(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 10

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(288)
class ImpactShot(AdditionalPerk, ActivePerk):
    points_cost: int = 10
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

    def on_gain(self, actor: "CharacterInstance") -> bool:
        ...

@dataclass
@register_perk(289)
class StrongBody(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5
    def apply_once(self, actor: "CharacterInstance") -> None:
        actor.max_hp += 5
        actor.hp += 5
        self.is_completed = True

@dataclass
@register_perk(290)
class Knockdown(AdditionalPerk, ActivePerk):
    points_cost: int = 10
    cooldown: int = 0

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(291)
class ISurvive(AdditionalPerk, PassiveTriggeredPerk):
    is_activated: bool = True
    usage_count: int = 1
    points_cost: int = 25

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(292)
class ScenarioShield(AdditionalPerk, PassiveTriggeredPerk):
    is_activated: bool = True
    usage_count: int = 1
    points_cost: int = 20

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(293)
class ThrowingKnives(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 25
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(294)
class HeavyArmor(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 10
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(295)
class BreakTime(AdditionalPerk, ActivePerk):
    points_cost: int = 10

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(296)
class SlidingShot(AdditionalPerk, ActivePerk):
    cooldown: int = 2
    points_cost: int = 15

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(297)
class VeteranShooter(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(298)
class Poisoner(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5

    def apply_once(self, actor: "CharacterInstance") -> None:
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[GasGrenade]))
        actor.inventory.add_to_specific_cell(cell, GasGrenade())
        self.is_completed = True

@dataclass
@register_perk(299) # TODO: Not actually impulse, product gap
class NapalmLover(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 5

    def apply_once(self, actor: "CharacterInstance") -> None:
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[ImpulseGrenade]))
        actor.inventory.add_to_specific_cell(cell, ImpulseGrenade())
        self.is_completed = True

@dataclass
@register_perk(300)
class RestlessFighter(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 10

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(301)
class ControlledFire(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 20

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(302)
class Interruption(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 10

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(303)
class Alertness(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(304)
class AntiTankWarhead(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 10
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(305)
class StickyMine(AdditionalPerk, ActivePerk):
    cooldown: int = 0
    points_cost: int = 10

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(306)
class ParamedicAdditional(AdditionalPerk, Paramedic):
    points_cost: int = 15


@dataclass
@register_perk(307)
class Cryogenic(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 10

    def apply_once(self, actor: "CharacterInstance") -> None:
        actor.available_consumables.append(Cryogen)
        cell = actor.inventory.add_cell(TypedInventoryCell(available_consumables=[Cryogen]))
        actor.inventory.add_to_specific_cell(cell, Cryogen())
        self.is_completed = True

@dataclass
@register_perk(308)
class Adrenaline(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 20

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(309)
class LayeredDefense(AdditionalPerk, PassiveOneTimePerk):
    points_cost: int = 30
    def apply_once(self, actor: "CharacterInstance") -> None:
        ...

@dataclass
@register_perk(310)
class KineticCharge(AdditionalPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(311)
class Absorption(AdditionalJediPerk, PassiveTriggeredPerk):
    points_cost: int = 15

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> None:
        pass


@dataclass
@register_perk(312)
class JediAdrenaline(AdditionalJediPerk, Adrenaline):
    points_cost: int = 20


@dataclass
@register_perk(313)
class Attraction(AdditionalJediPerk, ForceActivePerk):
    cooldown: int = 0
    points_cost: int = 15
    use_force_points = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(314)
class JediMoves(AdditionalJediPerk, Parkour):
    points_cost: int = 5

@dataclass
@register_perk(315)
class BreakWeapon(AdditionalJediPerk, ForceActivePerk):
    points_cost: int = 10
    use_force_points = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(316)
class JediScenarioShield(AdditionalJediPerk, ScenarioShield):
    pass

@dataclass
@register_perk(317)
class ForceBoost(AdditionalJediPerk, ForceActivePerk):
    points_cost: int = 20
    use_force_points = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(318)
class ForceStabilize(AdditionalJediPerk, ForceActivePerk):
    points_cost: int = 15
    use_force_points = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(319)
class JediStrongBody(AdditionalJediPerk, StrongBody):
    pass

@dataclass
@register_perk(320)
class JediHiddenReserves(AdditionalJediPerk, HiddenReserves):
    pass

@dataclass
@register_perk(321)
class ForceUnity(AdditionalJediPerk, PassiveTriggeredPerk):
    points_cost: int = 15
    is_activated: bool = True

    def conditions_met(self, actor: "ForceUser", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ForceUser", ctx: Optional[EventCtx]) -> None:
        actor.max_force_points += 1

@dataclass
@register_perk(322)
class Swordmaster(AdditionalJediPerk, PassiveOneTimePerk):
    points_cost: int = 10
    def apply_once(self, actor: "CharacterInstance") -> None:
        actor.main_weapon.base_acc += 10
        actor.main_weapon.base_dices.append(Dice(4))
        self.is_completed = True

@dataclass
@register_perk(323)
class ForceJump(AdditionalJediPerk, ForceActivePerk):
    points_cost: int = 10
    use_force_points = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(324)
class JediLickingWoundsAdditional(AdditionalJediPerk, LickingWounds):
    ...

@dataclass
@register_perk(325)
class ForceBind(AdditionalJediPerk, ForceActivePerk):
    points_cost: int = 20
    use_force_points = 2

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(326)
class JediSprinter(AdditionalJediPerk, Sprinter):
    ...

@dataclass
@register_perk(327)
class ForceMaster(AdditionalJediPerk, PassiveOneTimePerk):
    points_cost: int = 25
    def apply_once(self, actor: "ForceUser") -> None:
        actor.max_force_points += 5
        actor.restore_force_points()
        self.is_completed = True

@dataclass
@register_perk(328)
class JediSelfSacrifice(AdditionalJediPerk, SelfSacrifice):
    ...

@dataclass
@register_perk(329)
class JediLayeredDefense(AdditionalJediPerk, LayeredDefense):
    ...

@dataclass
@register_perk(330)
class StrikeFlurry(AdditionalJediPerk, ForceActivePerk):
    points_cost: int = 20
    use_force_points = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(331)
class ElectrostaffStrike(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(332)
class WideSwing(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(333)
class EnergyFlow(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 0

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ElectricGuard", ctx: Optional[EventCtx]) -> None:
        actor.add_overload()

@dataclass
@register_perk(334)
class LightweightFighter(ActivePerk):
    cooldown: int = 3

    def on_gain(self, actor: "CharacterInstance") -> None:
        actor.mobility += 10
        actor.dodge += 15

    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(335)
class StaffMastery(PassiveTriggeredPerk):
    is_activated: bool = True
    cooldown: int = 1

    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ElectricGuard", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(336)
class PiercingSpear(ActivePerk):
    def on_activate(self, actor, *args, **kwargs):
        return True

@dataclass
@register_perk(337)
class Parry(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ElectricGuard", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(338)
class OverloadSurge(ActivePerk):
    cooldown: int = 1

    def ready(self) -> bool:
        if self.owner.overload_points < 2:
            return False
        return super().ready()

    def on_activate(self, actor: "ElectricGuard", *args, **kwargs):
        actor.use_overload(2)
        return True

@dataclass
@register_perk(339)
class ModifiedGear(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ElectricGuard", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(340)
class BattleReady(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ElectricGuard", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(341)
class FirstStrike(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ElectricGuard", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(342)
class ControlZone(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ElectricGuard", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(343)
class GetOverHere(ActivePerk):

    def on_activate(self, actor: "ElectricGuard", *args, **kwargs):
        return True

@dataclass
@register_perk(344)
class StaffGrab(ActivePerk):
    cooldown: int = 1

    def on_activate(self, actor: "ElectricGuard", *args, **kwargs):
        return True

@dataclass
@register_perk(345)
class LightningDash(ActivePerk):
    cooldown: int = 3

    def on_activate(self, actor: "ElectricGuard", *args, **kwargs):
        return True

@dataclass
@register_perk(346)
class JuryRiggedShieldGenerator(ActivePerk):
    def on_activate(self, actor: "ElectricGuard", *args, **kwargs):
        actor.use_overload()
        return True

@dataclass
@register_perk(347)
class Reaper(ActivePerk):
    cooldown: int = 4

    def on_activate(self, actor: "ElectricGuard", *args, **kwargs):
        return True

@dataclass
@register_perk(348)
class Thunderwave(PassiveTriggeredPerk):
    def conditions_met(self, actor: "CharacterInstance", ctx: Optional[EventCtx]) -> bool:
        return True

    def apply_effect(self, actor: "ElectricGuard", ctx: Optional[EventCtx]) -> None:
        pass

@dataclass
@register_perk(349)
class AllOutPush(ActivePerk):
    cooldown: int = 2

    def on_activate(self, actor: "ElectricGuard", *args, **kwargs):
        return True

@dataclass
@register_perk(350)
class Stormbreaker(ActivePerk):
    def on_activate(self, actor: "ElectricGuard", *args, **kwargs):
        actor.use_overload(5)
        return True

    def ready(self) -> bool:
        if self.owner.overload_points < 5:
            return False
        return super().ready()
