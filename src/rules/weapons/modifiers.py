from dataclasses import dataclass
from typing import Optional


@dataclass
class DistanceModifier:
    """
    Represents how weapon performance changes depending on distance.

    max_distance: The maximum distance (inclusive) for this rule to apply. 
                  If None, it means "any distance beyond the last rule".
    damage_mult:  Multiplier applied to base damage (e.g., 2/3 for reduced damage).
    accuracy_buff: Additive accuracy modifier in percentage points (relative to 100% base).
    cr_buff:      Additive critical hit chance modifier in percentage points.
    distance_step: Additional change applied for every step beyond max_distance 
                   (only relevant if max_distance is None).
    is_effective: True if this is considered the optimal range.
    """
    max_distance: Optional[int]
    damage_mult: float = 1
    accuracy_buff: int = 0
    cr_buff: int = 0
    distance_step: int = 0
    is_effective: bool = False


# Cover penalty constants
HALF_COVER_PENALTY = 20
FULL_COVER_PENALTY = 45
