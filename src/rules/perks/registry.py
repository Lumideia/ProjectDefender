from typing import Dict, Type, Iterable

PERK_REGISTRY: Dict[int, Type["Perk"]] = {}   # registry to store all create perks (stable)


def register_perk(perk_id: int):
    """dec for registry"""

    def decorator(cls: Type["Perk"]):
        if perk_id in PERK_REGISTRY:
            raise ValueError(f"Perk id {perk_id} used") # TODO: Delete later maybe
        PERK_REGISTRY[perk_id] = cls
        cls.perk_id = perk_id
        return cls
    return decorator

def create_perk(perk_id: int, **kwargs) -> "Perk":
    return PERK_REGISTRY.get(perk_id)(**kwargs)

def list_registered_ids() -> Iterable[int]:
    return PERK_REGISTRY.keys()
