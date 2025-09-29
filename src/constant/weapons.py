from src.rules.weapons.weapon import FirearmWeapon, MeleeWeapon, ThrowingWeapon, MachineGun
from src.rules.weapons.modifiers import DistanceModifier
from src.rules.dice import Dice

MAIN_WEAPONS = [
FirearmWeapon(
        name="DP-23 Shotgun",
        base_atk=0,
        base_dices=[Dice(4)] * 5,
        cr_dices=[Dice(8)],
        movement_effects=0,
        armor_destroying=0,
        is_move_attack_allowed=False,
        mag_size=6,
        distance_rules=[
            DistanceModifier(0, accuracy_buff=0, cr_buff=60),
            DistanceModifier(5, accuracy_buff=0, cr_buff=30),
            DistanceModifier(15, accuracy_buff=-20, damage_mult=2 / 3),
            DistanceModifier(30, accuracy_buff=-40, damage_mult=1 / 3, distance_step=20)
        ],
        reload_cost=1,
        is_heavy=False
    ),
    FirearmWeapon(
        name="DC-15A",
        base_atk=0,
        base_dices=[Dice(6), Dice(8)],
        cr_dices=[Dice(6)],
        movement_effects=0,
        armor_destroying=0,
        is_move_attack_allowed=False,
        mag_size=5,
        distance_rules=[
            DistanceModifier(0, accuracy_buff=-20),
            DistanceModifier(30, cr_buff=20),
            DistanceModifier(80, accuracy_buff=-10),
            DistanceModifier(120, accuracy_buff=-20, damage_mult=1 / 3),
        ],
        reload_cost=1,
        is_heavy=True
    ),
    FirearmWeapon(
        name="DC-15S",
        base_dices=[Dice(4), Dice(8)],
        cr_dices=[Dice(6)],
        mag_size=7,
        distance_rules=[
            DistanceModifier(0, accuracy_buff=-10),
            DistanceModifier(10, accuracy_buff=0, cr_buff=20),
            DistanceModifier(60, accuracy_buff=-10),
            DistanceModifier(80, accuracy_buff=-20, distance_step=20)
        ]
    ),
    FirearmWeapon(
        name="DC-17M",
        base_dices=[Dice(6), Dice(4), Dice(4), Dice(4)],
        cr_dices=[Dice(10)],
        mag_size=7,
        distance_rules=[
            DistanceModifier(0, accuracy_buff=-10),
            DistanceModifier(10, accuracy_buff=0, cr_buff=30),
            DistanceModifier(60, accuracy_buff=-10),
            DistanceModifier(80, accuracy_buff=-20, distance_step=20)
        ]
    ),
    FirearmWeapon(
        name="DC-17",
        base_dices=[Dice(8)],
        cr_dices=[Dice(4)],
        mag_size=7,
        distance_rules=[
            DistanceModifier(0, cr_buff=20),
            DistanceModifier(40, accuracy_buff=-5),
            DistanceModifier(60, accuracy_buff=-15, distance_step=10),
        ]
    ),
    MachineGun(
        name="Z6",
        base_atk=3,
        base_dices=[Dice(6), Dice(6), Dice(6)],
        cr_dices=[Dice(6)],
        mag_size=7,
        distance_rules=[
            DistanceModifier(0, accuracy_buff=-20),
            DistanceModifier(15, accuracy_buff=0, cr_buff=10),
            DistanceModifier(50, accuracy_buff=-10),
            DistanceModifier(70, accuracy_buff=-15, damage_mult=2 / 3, distance_step=20)
        ],
        is_heavy=True,
    ),
    FirearmWeapon(
        name="Огнестрел 773",
        base_atk=5,
        base_dices=[Dice(6), Dice(6), Dice(6)],
        cr_dices=[Dice(10)],
        movement_effects=0,
        armor_destroying=0,
        is_move_attack_allowed=False,
        mag_size=5,
        distance_rules=[
            DistanceModifier(0, accuracy_buff=-30, cr_buff=0),
            DistanceModifier(40, accuracy_buff=-5, cr_buff=0),
            DistanceModifier(60, accuracy_buff=10, cr_buff=20),
            DistanceModifier(120, accuracy_buff=20, cr_buff=20),
            DistanceModifier(300, accuracy_buff=-10, cr_buff=0, distance_step=10),
        ],
        reload_cost=1,
        is_heavy=True
    ),
]


OTHER_WEAPONS = [
    FirearmWeapon(
        name='УЗЧ',
        base_dices=[Dice(8), Dice(8), Dice(8)],
        cr_dices=[Dice(10), Dice(10)],
        distance_rules=[
            DistanceModifier(0, accuracy_buff=0, cr_buff=60),
            DistanceModifier(15, accuracy_buff=-20, damage_mult=2 / 3),
            DistanceModifier(30, accuracy_buff=-40, damage_mult=1 / 3, distance_step=20)
        ],
        mag_size=2,
        is_heavy=False
    ),
    MeleeWeapon(
        name='Нож',
        base_dices=[Dice(4), Dice(4)],
        cr_dices=[Dice(4)],
        base_cr=15,
        distance_rules=None,
        movement_effects=0,
        armor_destroying=0,
    ),
    MeleeWeapon(
        name='Щит',
        base_atk = -1,
        base_dices=[Dice(4)],
        cr_dices=[Dice(4)],
        base_cr=10,
        distance_rules=None,
    ),
    MeleeWeapon(
        name='Дубинка',
        base_dices=[Dice(4), Dice(4)],
        cr_dices=[Dice(4)],
        base_cr=10,
        distance_rules=None,
    ),
    MeleeWeapon(
        name='Световой меч',
        base_atk=5,
        base_dices=[Dice(10), Dice(10)],
        cr_dices=[Dice(6)],
        base_cr=15,
        distance_rules=None,
        base_acc = 90
    ),
    ThrowingWeapon(
        name='Нож мет.',
        base_dices=[Dice(4), Dice(4)],
        cr_dices=[Dice(4)],
        max_distance=40,
        distance_rules=[
            DistanceModifier(0, accuracy_buff=0, cr_buff=15),
            DistanceModifier(40, accuracy_buff=-100, damage_mult=0),
        ],
        movement_effects=0,
        armor_destroying=0,
        base_count=2
    ),
    MeleeWeapon(
        name='Электропосох',
        base_dices=[Dice(8), Dice(8)],
        base_atk=5,
        cr_dices=[Dice(8)],
        base_cr=15,
        base_acc=90,
        bonus_dices=[]
    ),
    MeleeWeapon(
        name='DC-17 (удар)',
        base_dices=[Dice(8)],
        base_cr=20,
        cr_dices=[Dice(4)],
        base_acc=80
    )
]
MAIN_WEAPONS_DICT = {weapon.name: weapon for weapon in MAIN_WEAPONS}

OTHER_WEAPONS_DICT = {weapon.name: weapon for weapon in OTHER_WEAPONS}
