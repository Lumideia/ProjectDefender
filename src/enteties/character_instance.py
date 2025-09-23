from dataclasses import dataclass, field
from typing import List, Dict, Type

from src.constant.world import WORLD_BUS
from src.enteties.weapon_instance import WeaponInstance
from src.rules.characters.character import Character
from src.rules.consumables.Inventory import Inventory
from src.rules.consumables.consumable import Consumable, DEFAULT_CONSUMABLES
from src.rules.effects.effect import Effect
from src.rules.perks.perk import Perk
from src.rules.events.types import Event
from src.rules.perks.registry import create_perk
from src.constant.weapons import MAIN_WEAPONS, OTHER_WEAPONS


@dataclass(eq=False)
class CharacterInstance:
    mobility: int = field(init=False)
    dodge: int = field(init=False)
    accuracy: int = field(init=False)
    observation: bool = False
    character: Character = field(default_factory=Character)
    hp: int = field(init=False)
    armour: int = field(init=False)
    main_weapon: WeaponInstance = field(default=None)
    side_weapon: WeaponInstance = field(default=None)
    perk_order: List[List[int]] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)
    available_consumables: List[Type[Consumable]] = field(default_factory=lambda: DEFAULT_CONSUMABLES)
    available_weapons = list()
    available_side_weapons = list()


    effects: List[Effect] = field(default_factory=list)
    perks: List[Perk] = field(default_factory=list)
    _perk_subs: Dict[Event, List[Perk]] = field(default_factory=dict, init=False, repr=False)
    max_tier_length: int = 5


    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other

    def find_perk_tier(self, p_id):
        for i, sublist in enumerate(self.perk_order):
            if p_id in sublist:
                return i
        return None

    def get_perk_by_id(self, p_id):
        return next((perk for perk in self.perks if perk.id == p_id), None)

    def __post_init__(self):
        WORLD_BUS.register_actor(self)
        self.hp = self.character.hp
        self.armour = self.character.armour
        self.mobility = self.character.movement
        self.dodge = self.character.dodge
        self.accuracy = self.character.accuracy
        self.main_weapon = None

    def creation_completed(self):
        if self.perks:
            return
        for tier_row in self.perk_order:
            for pid in tier_row:
                self.add_perk(create_perk(pid))

    def add_perk(self, perk: "Perk"):
        perk.is_taken = None
        perk.owner = self
        self.perks.append(perk)
        if not perk.is_main_perk:
            self.add_additional_perk_to_order(perk)
            self.activate_perk(perk)
        elif perk.id in self.perk_order[0]:
            self.activate_perk(perk)


    def activate_perk(self, perk: "Perk"):
        if perk.is_taken is not None:
            return

        perk.is_taken = True
        perk.on_gain(self)

        for ev in perk.events():
            self._perk_subs.setdefault(ev, []).append(perk)
            WORLD_BUS.on_perk_added(self, ev)

        tier = self.find_perk_tier(perk.id)
        if tier and perk.is_main_perk:
            for p_id in self.perk_order[tier]:
                if p_id != perk.id:
                    same_tier_perk = next((p for p in self.perks if p.id == p_id), None)
                    same_tier_perk.is_taken = False

    def add_additional_perk_to_order(self, perk: "Perk"):
        if self.perks[-2].is_main_perk or len(self.perk_order[-1]) == self.max_tier_length:
            self.perk_order.append([perk.id])
        else:
            self.perk_order[-1].append(perk.id)


    def remove_perk(self, perk: "Perk") -> None:
        if perk in self.perks:
            self.perks.remove(perk)

        for ev in perk.events():
            lst = self._perk_subs.get(ev, [])
            self._perk_subs[ev] = [p for p in lst if p is not perk]
            WORLD_BUS.on_perk_removed(self, ev)
            if not self._perk_subs[ev]:
                del self._perk_subs[ev]


    def notify(self, ev: Event, ctx):
        if ev == Event.TURN_END:
            for perk in self.perks:
                perk.tick()
        else:
            for perk in self._perk_subs.get(ev, ()):
                perk.try_trigger(self, ctx)

    def tick_perks(self):
        for p in self.perks:
            p.tick()

    def on_turn_start(self, turn_idx: int):
        for p in self.perks:
            if hasattr(p, "on_turn_start"):
                p.on_turn_start(turn_idx)

    def on_turn_end(self, turn_idx: int):
        for p in self.perks:
            if hasattr(p, "on_turn_end"):
                p.on_turn_end(turn_idx)

    def set_main_weapon(self, weapon: "WeaponInstance"):
        if any(weapon.weapon.name == w.name for w in self.available_weapons):
            self.main_weapon = weapon

    def set_side_weapon(self, weapon: "WeaponInstance"):
        if any(weapon.weapon.name == w .name for w in self.available_side_weapons):
            self.side_weapon = weapon


@dataclass(eq=False)
class Grenadier(CharacterInstance):
    class_name: str = "Гренадёр"
    available_weapons = [MAIN_WEAPONS[1], MAIN_WEAPONS[2]]
    available_side_weapons = [None]
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [1, 87, 3, 2],
        [4, 5, 86, 6],
        [88, 7, 8, 9],
        [51, 52, 10, 53],
        [11, 89, 54, 90]
    ])

    base_hp: int = 30
    base_armour: int = 5


@dataclass(eq=False)
class MachineGunner(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[5]]
    available_side_weapons = [None]
    class_name: str = "Пулемётчик"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [91, 92, 12, 94],
        [95, 13, 14, 15],
        [96, 93, 55, 16],
        [97, 98, 56, 57],
        [99, 100, 58, 101]
    ])

@dataclass(eq=False)
class FlyingSoldier(CharacterInstance):
    class_name: str = "Летающий солдат"
    available_weapons =  [MAIN_WEAPONS[1], MAIN_WEAPONS[2], MAIN_WEAPONS[5], MAIN_WEAPONS[6]]
    available_side_weapons = [None]
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [102, 17, 103, 104],
        [59, 18, 19, 60],
        [61, 20, 21, 62],
        [63, 22, 23, 105],
        [24, 106, 107, 108]
    ])
    consumable_count: int = field(default=0)
    character: Character = field(default_factory=Character)

@dataclass(eq=False)
class Officer(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[4]]
    available_side_weapons = [None]
    class_name: str = "Офицер"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [25, 26, 110, 109, 111],
        [112, 27, 64, 113],
        [28, 65, 66, 114],
        [67, 68, 162, 115],
        [116, 117, 163, 118]
    ])

@dataclass(eq=False)
class Engineer(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[1], MAIN_WEAPONS[2]]
    available_side_weapons = [None]
    class_name: str = "Инженер"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [175, 176, 177, 178, 179],
        [180, 181, 182, 183],
        [184, 185, 186, 187],
        [188, 189, 190, 191],
        [192, 193, 194, 195]
    ])

@dataclass(eq=False)
class Stormtrooper(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[0]]
    available_side_weapons = [None]
    class_name: str = "Штурмовик"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [119, 29, 59, 156],
        [120, 69, 70, 71],
        [72, 73, 74, 121],
        [122, 123, 96, 75],
        [124, 160, 58, 157],
    ])

@dataclass(eq=False)
class Shooter(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[1], MAIN_WEAPONS[2]]
    available_side_weapons = [MAIN_WEAPONS[4], OTHER_WEAPONS[0]]
    class_name: str = "Застрельщик"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [76, 77, 15, 125, 30],
        [31, 78, 79, 80, 32],
        [126, 95, 81, 127, 82],
        [128, 96, 83, 56, 84],
        [129, 58, 85, 24, 169]
    ])
    def set_side_weapon(self, weapon: "WeaponInstance"): # TODO: Think how to not delete
        """Class have special perks related to specific weapons"""
        if weapon.weapon.name == self.available_side_weapons[0].name:
            for perk_tier in self.perk_order:
                perk_tier.pop(-1)

        elif weapon.weapon.name == self.available_side_weapons[1].name:
            for perk_tier in self.perk_order:
                perk_tier.pop(0)

        else:
            return
        self.side_weapon = weapon


@dataclass(eq=False)
class Sniper(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[1], MAIN_WEAPONS[6]]
    available_side_weapons = [MAIN_WEAPONS[4], None]
    class_name: str = "Снайпер"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [216, 130, 131, 217],
        [152, 33, 218, 34],
        [159, 35, 132, 74],
        [133, 219, 134, 158],
        [135, 136, 137, 100]
    ])

@dataclass(eq=False)
class Scout(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[4]]
    available_side_weapons = [OTHER_WEAPONS[5]]
    class_name: str = "Разведчик"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [138, 220, 221, 36],
        [139, 122, 37, 222],
        [38, 229, 140, 223],
        [40, 161, 39, 126],
        [224, 58, 141, 129]
    ])

@dataclass(eq=False)
class Medic(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[1], MAIN_WEAPONS[2]]
    available_side_weapons = [None]
    class_name: str = "Медик"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [41, 42, 43, 142],
        [149, 122, 44, 143],
        [45, 33, 150, 144],
        [151, 145, 46, 146],
        [47, 225, 147, 148]
    ])
@dataclass(eq=False)
class ShieldSoldier(CharacterInstance):
    available_weapons =  [MAIN_WEAPONS[4]]
    available_side_weapons = [OTHER_WEAPONS[2]]
    class_name: str = "Шитоносец"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [164, 165, 153, 48, 166],
        [167, 154, 172, 226],
        [168, 123, 227, 230],
        [49, 155, 228, 170],
        [171, 173, 174, 50]
    ])

@dataclass(eq=False)
class ForceUser(CharacterInstance):
    available_weapons =  [OTHER_WEAPONS[4]]
    available_side_weapons = [None]
    class_name: str = "Джедай"
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [196, 197, 198, 59, 199],
        [200, 201, 202, 203],
        [204, 205, 206, 207],
        [208, 209, 210, 211],
        [212, 213, 214, 215],
    ])

CHARACTER_CLASSES = [
    Grenadier,
    MachineGunner,
    FlyingSoldier,
    Officer,
    Engineer,
    Stormtrooper,
    Shooter,
    Sniper,
    Scout,
    Medic,
    ShieldSoldier,
    ForceUser,
]
