from dataclasses import dataclass

HALF_COVER_PENALTY = 20
FULL_COVER_PENALTY = 45

@dataclass
class CoverCounts:
    half: int = 0
    full: int = 0

    def total_penalty(self) -> int:
        h = max(0, self.half)
        f = max(0, self.full)
        return h * HALF_COVER_PENALTY + f * FULL_COVER_PENALTY

# TODO: Implement in main.py
