from abc import ABC
from dataclasses import dataclass, field
from typing import List, Dict

from src.enteties.weapon_instance import WeaponInstance
from src.rules.characters.character import Character
from src.rules.effects.effect import Effect
from src.rules.effects.perks.perk import PassiveTriggeredPerk, Perk, PassiveOneTimePerk
from src.rules.events.types import Event


@dataclass
class CharacterInstance:
    character: Character = field(init=False)
    hp: int = field(init=False)
    armour: int = field(init=False)
    main_weapon: WeaponInstance = field(init=False)
    side_weapon: WeaponInstance = field(init=False, default=None)


    effects: List[Effect] = field(default_factory=list)
    perks: List[Perk] = field(default_factory=list)
    _perk_subs: Dict[Event, List[PassiveTriggeredPerk]] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        self.hp = self.character.hp
        self.armour = self.character.armour

    def add_perk(self, perk: "Perk"):
        self.perks.append(perk)
        perk.on_gain(self)
        if isinstance(perk, PassiveTriggeredPerk):
            for ev in perk.events():
                self._perk_subs.setdefault(ev, []).append(perk)

    def notify(self, ev: Event, ctx):
        for perk in self._perk_subs.get(ev, ()):
            perk.try_trigger(self, ctx)

    def tick_perks(self):
        for p in self.perks:
            p.tick()
