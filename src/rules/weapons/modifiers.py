from dataclasses import dataclass
from typing import Optional


@dataclass
class DistanceModifier:
    """
    Represents how weapon performance changes depending on distance.

    min_distance: The minimum distance (inclusive) for this rule to apply.
                  If None, it means "any distance beyond the last rule".
    damage_mult:  Multiplier applied to base damage (e.g., 2/3 for reduced damage).
    accuracy_buff: Additive accuracy modifier in percentage points (relative to 100% base).
    cr_buff:      Additive critical hit chance modifier in percentage points.
    distance_step: Additional change applied for every step beyond max_distance 
                   (only relevant if max_distance is None).
    is_effective: True if this is considered the optimal range.
    """
    min_distance: Optional[int]
    damage_mult: float = 1
    accuracy_buff: int = 0
    cr_buff: int = 0
    distance_step: int = 0
    is_effective: bool = False

    def calculate_penalties(self, distance: int) -> tuple[float, int, int]:
        """
        Calculate the final damage multiplier, accuracy buff, and crit buff
        for a given distance, including step-based adjustments for ranges
        beyond max_distance.

        Returns:
            (damage_mult, accuracy_penalty, cr_penalty)
        """
        acc_penalty = self.accuracy_buff
        if self.distance_step > 0:
            extra_distance = distance - self.min_distance
            steps = extra_distance // self.distance_step
            acc_penalty += steps * self.accuracy_buff

        return self.damage_mult, acc_penalty, self.cr_buff
