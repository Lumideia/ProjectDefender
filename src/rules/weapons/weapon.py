from abc import ABC

from src.rules.dice import Dice
from src.rules.weapons.modifiers import DistanceModifier


class Weapon(ABC):
    def __init__(
            self,
            base_dices: list[Dice] = None,
            cr_dices: list[Dice] = None,
            movement_effects: int = 0,
            armor_destroying: int = 0,
            is_move_attack_allowed: bool = False,
    ):
        self.base_dices = base_dices
        self.cr_dices = cr_dices
        self.movement_effects = movement_effects
        self.armor_destroying = armor_destroying
        self.is_move_attack_allowed = is_move_attack_allowed


class FirearmWeapon(Weapon):
    base_atk: int = 0
    mag_size: int
    distance_rules: list[DistanceModifier]
    reload_cost: int = 1
    is_heavy: bool = False

    def __init__(
            self,
            base_dices: list[Dice] = None,
            cr_dices: list[Dice] = None,
            movement_effects: int = 0,
            armor_destroying: int = 0,
            is_move_attack_allowed: bool = False,
            base_atk: int = 0,
            mag_size: int = 20,
            distance_rules: list[DistanceModifier] = None,
            reload_cost: int = 1,
            is_heavy: bool = False
    ):
        super().__init__(base_dices, cr_dices, movement_effects, armor_destroying, is_move_attack_allowed)
        self.base_atk = base_atk
        self.mag_size = mag_size
        self.distance_rules = sorted(
            distance_rules,
            key=lambda r: float('inf') if r.max_distance is None else r.max_distance
        )
        self.reload_cost = reload_cost
        self.is_heavy = is_heavy


    def get_distance_rule(self, distance):
        for rule in self.distance_rules:
            if rule.max_distance is None:
                return rule
            if distance <= rule.max_distance:
                return rule
        raise Exception('Invalid distance. Probably wrong weapon setting')


class ThrowingWeapon(Weapon):
    max_distance: int = 30

    def __init__(
            self,
            base_dices: list[Dice] = None,
            cr_dices: list[Dice] = None,
            movement_effects: int = 0,
            armor_destroying: int = 0,
            is_move_attack_allowed: bool = False,
            max_distance: int = 30,
    ):
        super().__init__(base_dices, cr_dices, movement_effects, armor_destroying, is_move_attack_allowed)
        self.max_distance = max_distance

class MeleeWeapon(Weapon):
    def __init__(
            self,
            base_dices: list[Dice] = None,
            cr_dices: list[Dice] = None,
            movement_effects: int = 0,
            armor_destroying: int = 0,
    ):
        super().__init__(base_dices, cr_dices, movement_effects, armor_destroying, is_move_attack_allowed=True)
