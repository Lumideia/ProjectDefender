from dataclasses import dataclass

from character import Character

@dataclass
class Operative(Character):
    rank: int = 0
