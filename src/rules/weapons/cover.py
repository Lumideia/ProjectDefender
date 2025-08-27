from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.constant.covers import (
    FULL_HIND_COVER_PENALTY, HALF_HIND_COVER_PENALTY, FULL_USED_COVER_PENALTY, HALF_USED_COVER_PENALTY
)


@dataclass
class Cover:
    is_full: Optional[bool] = None  # Whether full or half

    def total_penalty(self) -> int:
        if self.is_full is not None:
            return FULL_USED_COVER_PENALTY if self.is_full else HALF_USED_COVER_PENALTY
        return 0

@dataclass
class Interference:
    half: int = 0
    full: int = 0

    def total_penalty(self, only_full: bool = False) -> int:
        h = 0 if only_full else max(0, self.half)
        f = max(0, self.full)
        return h * HALF_HIND_COVER_PENALTY + f * FULL_HIND_COVER_PENALTY


class Position(Enum):
    LOWER = 1
    EQUAL = 2
    HIGHER = 3
