from collections import defaultdict
from typing import Dict, Set, List, TYPE_CHECKING
from src.rules.events.types import Event, EventCtx, CharacterEvent

if TYPE_CHECKING:
    from src.enteties.character_instance import CharacterInstance

class EventBus:
    def __init__(self):
        self._actors: Set["CharacterInstance"] = set()
        # way to store specific event listeners
        self._index: Dict[Event, Set["CharacterInstance"]] = defaultdict(set)

    def register_actor(self, actor: "CharacterInstance") -> None:
        self._actors.add(actor)
        self._reindex_actor(actor)

    def unregister_actor(self, actor: "CharacterInstance") -> None:
        if actor in self._actors:
            self._actors.remove(actor)
        for ev in list(self._index.keys()):
            self._index[ev].discard(actor)

    def _reindex_actor(self, actor: "CharacterInstance") -> None: #TODO: Not sure if it will be needed
        for ev in list(self._index.keys()):
            self._index[ev].discard(actor)

        for ev, perks in actor._perk_subs.items():
            if perks:
                self._index[ev].add(actor)

    def on_perk_added(self, actor: "CharacterInstance", ev: Event) -> None:
        if actor in self._actors:
            self._index[ev].add(actor)

    def on_perk_removed(self, actor: "CharacterInstance", ev: Event) -> None:
        if actor in self._actors:
            if not actor._perk_subs.get(ev):
                self._index[ev].discard(actor)

    # --- рассылка ---

    def broadcast(self, ev: Event, ctx: EventCtx):
        """
        Notify only specific candidates
        """
        if ev == Event.TURN_END:
            candidates = list(self._actors)
        else:
            candidates = list(self._index.get(ev, ()))
        for owner in candidates:
            #TODO: create filters for notifying less characters (radius for aura, team/enemy etc)
            owner.notify(ev, ctx)

    # Example
    def _nearby(self, owner: "CharacterInstance", ctx: EventCtx, radius: int = 12) -> bool:
        pass
        if isinstance(ctx, CharacterEvent):
            ax, ay = owner.x, owner.y
            bx, by = ctx.actor.x, ctx.actor.y
            dx, dy = ax - bx, ay - by
            return dx*dx + dy*dy <= radius*radius
        return True
