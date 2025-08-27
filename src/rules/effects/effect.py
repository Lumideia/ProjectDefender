from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.rules.characters.character import Character


@dataclass
class Effect(ABC):
    is_negative: bool = False
    duration: int = 1

    @abstractmethod
    def apply_effect(self, target: Character) -> None:
        pass
