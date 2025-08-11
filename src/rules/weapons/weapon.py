from abc import ABC
from typing import List

from src.rules.dice import Dice
from src.rules.weapons.modifiers import DistanceModifier


class Weapon(ABC):
    def __init__(
            self,
            name: str = '',
            base_dices: List[Dice] = None,
            cr_dices: List[Dice] = None,
            movement_effects: int = 0,
            armor_destroying: int = 0,
            is_move_attack_allowed: bool = False,
            base_atk: int = 0,
    ):
        self.name = name
        self.base_dices = base_dices
        self.cr_dices = cr_dices
        self.movement_effects = movement_effects
        self.armor_destroying = armor_destroying
        self.is_move_attack_allowed = is_move_attack_allowed
        self.base_atk = base_atk


class FirearmWeapon(Weapon):
    def __init__(
            self,
            name: str = '',
            base_dices: List[Dice] = None,
            cr_dices: List[Dice] = None,
            movement_effects: int = 0,
            armor_destroying: int = 0,
            is_move_attack_allowed: bool = False,
            base_atk: int = 0,
            mag_size: int = 20,
            distance_rules: List[DistanceModifier] = None,
            reload_cost: int = 1,
            is_heavy: bool = False
    ):
        super().__init__(
            name, base_dices, cr_dices, movement_effects, armor_destroying, is_move_attack_allowed, base_atk
        )

        self.mag_size = mag_size
        self.distance_rules = sorted(
            distance_rules,
            key=lambda r: r.min_distance,
            reverse=True
        )
        self.reload_cost = reload_cost
        self.is_heavy = is_heavy


    def get_distance_rule(self, distance):
        for rule in self.distance_rules:
            if distance > rule.min_distance:
                return rule
        raise Exception('Invalid distance. Probably wrong weapon setting')


class ThrowingWeapon(Weapon):
    def __init__(
            self,
            name: str = '',
            base_dices: List[Dice] = None,
            cr_dices: List[Dice] = None,
            movement_effects: int = 0,
            armor_destroying: int = 0,
            is_move_attack_allowed: bool = False,
            base_atk: int = 0,
            max_distance: int = 30,
    ):
        super().__init__(
            name, base_dices, cr_dices, movement_effects, armor_destroying, is_move_attack_allowed, base_atk
        )
        self.max_distance = max_distance

class MeleeWeapon(Weapon):
    def __init__(
            self,
            name: str = '',
            base_dices: List[Dice] = None,
            cr_dices: List[Dice] = None,
            movement_effects: int = 0,
            armor_destroying: int = 0,
            base_atk: int = 0,
    ):
        super().__init__(
            name, base_dices, cr_dices, movement_effects, armor_destroying,
            is_move_attack_allowed=True, base_atk=base_atk
        )
