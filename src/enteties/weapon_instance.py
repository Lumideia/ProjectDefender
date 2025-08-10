from src.rules.weapons.weapon import FirearmWeapon


class FireArmWeaponInstance:
    def __init__(self, weapon: FirearmWeapon):
        self.weapon = weapon
        self.current_ammo = weapon.mag_size

    def shoot(self):
        if self.current_ammo > 0:
            self.current_ammo -= 1

    def reload(self):
        self.current_ammo = self.weapon.mag_size
