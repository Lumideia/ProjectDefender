class Calculation:
    def __init__(self, attack = None, defense = None, distance: int = 0):
        self.attack = attack
        self.distance_rule = attack.weapon.get_distance_rule(distance)
        self.defense = defense
        self.distance = distance

    def calculate_accuracy(self):
        base_acc = self.attack.accuracy - self.defense.accuracy
        if self.distance_rule.accuracy_abs:
            return base_acc + self.distance_rule.accuracy_buff
        return base_acc * self.distance_rule.accuracy_buff

    def calculate_cr(self):
        return self.attack.cr - self.defense.cr + self.distance_rule.cr_buff
