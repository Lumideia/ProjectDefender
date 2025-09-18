from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CharacterSize(Enum):
    SMALL = 1
    MEDIUM = 2
    HUGE = 3


@dataclass
class Consumable(ABC):
    class_name: str = None
    description: str = None
    max_count: Optional[int] = 5
    throw_distance: int = 30
    radius: int = 15
    ends_turn: bool = False
    default = True

    def apply(self):
        pass

class Grenade(Consumable):
    ...

@dataclass
class ThermalDetonator(Consumable):
    class_name: str = "Терм детонатор"
    description: str = "Стандартная боевая граната, имеющая диаметр взрыва 15 футов. Может быть брошена на расстояние до 30 футов. Дистанция броска считается к эпицентру взрыва. Бросок заканчивает ход. Наносит: 3д6 единиц урона"
    def apply(self):
        pass

@dataclass
class EMIGrenade(Grenade):
    class_name: str = "ЭМИ граната"
    description: str = "Специализированная боевая граната, не наносящая урона для органики. Диаметр взрыва равен 15 футов. Может быть брошена на расстояние до 30 футов. Дистанция броска считается к эпицентру взрыва. Бросок заканчивает ход. Наносит: 3д8 урона механизированным целям и имеет 20% разрядить энергетическое оружие. С шансом 90% выключает на один ход энергетические щиты"
    def apply(self):
        pass

@dataclass
class BaktaSpray(Consumable):
    class_name: str = "Бакта спрей"
    description: str = "Балончик особого целительного вещества, бакты, что гарантирует восстановление путем распыления на рану. Восстанавливает 3д4 единицы здоровья цели. Применение бакта спрея тратит одно действие, выполняется в непосредственной близости к раненой цели"

    def apply(self):
        pass


@dataclass
class Smoke(Grenade):
    class_name: str = "Дымовая"
    description: str = "Стандартная вспомогательная граната создающая область задымления, уменьшающую шансы при стрельбе как по целям в ней, так и при стрельбе сквозь неё на 20%. Диаметр взрыва равен 15 футов. Может быть брошена на расстояние до 30 футов. Дистанция броска считается к эпицентру взрыва. Бросок заканчивает ход"

    def apply(self):
        pass


@dataclass
class EnergeticWeb(Consumable):
    class_name: str = "Энерго сеть"
    description: str = "Частое снаряжение контрабандистов. Бросается как сетка на одну цель, бьёт опутанную цель током. Можно бросить на 20 футов с шансом 90%. Опутанная цель не может двигаться. Оружие цели с шансом 30% разряжается. С шансом 30% теряет сознание. Каждый ход что цель находиться под сетью, шансы потерять сознание и разрядить оружие растут на 10%. Для дроидов шанс отключения растет на 20% каждый ход. Снять сеть тратит полный ход. Бросок тратит одно действие"

    def apply(self):
        pass


@dataclass
class Flashing(Grenade):
    class_name: str = "Свето звуковая"
    description: str = "Стандартная вспомогательная граната, создающая яркую вспышку сопровождаемую крайне высокочастотным звуком. Накладывает дезориентацию на всех органических противников в диаметре 25 футов от места взрыва. Может быть брошена на расстояние до 40 футов. Дистанция броска считается к эпицентру взрыва. Бросок заканчивает ход"

    def apply(self):
        pass


@dataclass
class GasGrenade(Consumable):
    class_name: str = "Газовая"
    description: str = "Стандартная боевая граната, создающая ядовитое облако в диаметре 15 футов. Облако висит 3 хода. Органические цели получают отравление, если проходят сквозь облако. Отравление: 1д6 урона на протяжении трёх ходов. Уменьшение мобильности на 10 футов. Уменьшение меткости на 10. Может быть брошена на расстояние до 30 футов. Дистанция броска считается к эпицентру взрыва. Бросок заканчивает ход"

    def apply(self):
        pass


@dataclass
class ImpulseGrenade(Grenade):
    class_name: str = "Импульс"
    description: str = "Стандартная вспомогательная грана, отбрасывающая цели в диаметре 15 футов от себя на дистанцию 10 футов. Отброшенный противник получает -10 уклонения. Если отброшенный противник является органическим и ударяется о преграду, он получает дезориентацию. Может быть брошена на расстояние до 30 футов. Дистанция броска считается к эпицентру взрыва. Бросок заканчивает ход"

    def apply(self):
        pass


DEFAULT_CONSUMABLES = [
    ThermalDetonator,
    EMIGrenade,
    BaktaSpray,
    Smoke,
    EnergeticWeb,
    Flashing,
    GasGrenade,
    ImpulseGrenade,
]
# @dataclass
# class ThermalDetonator(Consumable):
#     class_name: str = "Термальный детонатор"
#     description: str = ""
#
# @dataclass
# class ThermalDetonator(Consumable):
#     class_name: str = "Термальный детонатор"
#     description: str = ""