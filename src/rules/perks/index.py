from src.rules.perks.perk import AdditionalPerk, AdditionalJediPerk
from src.rules.perks.registry import PERK_REGISTRY
from src.rules.perks.description.active import ACTIVE_PERKS
from src.rules.perks.description.passive import PASSIVE_PERKS
from src.rules.perks.description.aura import AURA_PERKS
from src.rules.perks.description.one_time import ONE_TIME_PERKS

def get_additional_perks():
    return [p() for p in PERK_REGISTRY.values() if issubclass(p, AdditionalPerk)]

def get_additional_jedi_perks():
    return [p for p in get_additional_perks() if isinstance(p, AdditionalJediPerk)]

def get_additional_common_perks():
    jedi_classes = {p for p in PERK_REGISTRY.values() if issubclass(p, AdditionalJediPerk)}
    return [p() for p in PERK_REGISTRY.values()
            if issubclass(p, AdditionalPerk) and p not in jedi_classes]

ALL_PERKS = {
    **ACTIVE_PERKS,
    **PASSIVE_PERKS,
    **AURA_PERKS,
    **ONE_TIME_PERKS,
}
