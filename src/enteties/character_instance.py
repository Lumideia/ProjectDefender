from dataclasses import dataclass, field
from typing import List, Dict

from src.constant.world import WORLD_BUS
from src.enteties.weapon_instance import WeaponInstance
from src.rules import perks
from src.rules.characters.character import Character
from src.rules.effects.effect import Effect
from src.rules.perks.perk import Perk
from src.rules.events.types import Event
from src.rules.perks.registry import create_perk
from src.constant.weapons import MAIN_WEAPONS
from src.rules.weapons.weapon import FirearmWeapon


@dataclass(eq=False)
class CharacterInstance:
    character: Character = field(init=False)
    hp: int = field(init=False)
    armour: int = field(init=False)
    main_weapon: WeaponInstance = field(init=False)
    side_weapon: WeaponInstance = field(init=False, default=None)


    effects: List[Effect] = field(default_factory=list)
    perks: List[Perk] = field(default_factory=list)
    _perk_subs: Dict[Event, List[Perk]] = field(default_factory=dict, init=False, repr=False)


    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other

    def __post_init__(self):
        WORLD_BUS.register_actor(self)
        self.hp = self.character.hp
        self.armour = self.character.armour

    def add_perk(self, perk: "Perk"):
        perk.owner = self
        self.perks.append(perk)
        perk.on_gain(self)
        for ev in perk.events():
            self._perk_subs.setdefault(ev, []).append(perk)
            WORLD_BUS.on_perk_added(self, ev)

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



AVAILABLE_FOR_GRENADIER = [
    w for w in MAIN_WEAPONS if w.name in ("DC-15A", "DC-15S")
]


@dataclass
class Grenadier(CharacterInstance):
    character: Character = field(default_factory=Character)
    selected_weapon: FirearmWeapon = field(
        default_factory=lambda: AVAILABLE_FOR_GRENADIER[0]
    )
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [1, 87, 3, 2],
        [4, 5, 86, 6],
        [88, 7, 8, 9],
        [51, 52, 10, 53],
        [11, 89, 54, 90]
    ])

    base_hp: int = 30
    base_armour: int = 5

    def __post_init__(self):
        # self.main_weapon = self.selected_weapon
        super().__post_init__()

        for tier_row in self.perk_order:
            for pid in tier_row:
                self.add_perk(create_perk(pid))


@dataclass
class Grenadier(CharacterInstance):

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other


    character: Character = field(default_factory=Character)
    selected_weapon: FirearmWeapon = field(
        default_factory=lambda: AVAILABLE_FOR_GRENADIER[0]
    )
    perk_order: List[List[int]] = field(default_factory=lambda: [
        [1, 87, 3, 2],
        [4, 5, 86, 6],
        [88, 7, 8, 9],
        [51, 52, 10, 53],
        [11, 89, 54, 90]
    ])

    base_hp: int = 30
    base_armour: int = 5

    def __post_init__(self):
        # self.main_weapon = self.selected_weapon
        super().__post_init__()

        for tier_row in self.perk_order:
            for pid in tier_row:
                self.add_perk(create_perk(pid))
