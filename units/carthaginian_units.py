# units/carthaginian_units.py

from units.base import Warrior, Archer, Cavalry

class CarthaginianWarrior(Warrior):
    def __init__(self, x, y):
        super().__init__("Карфагенский воин", 100, 27, x, y)

class CarthaginianArcher(Archer):
    def __init__(self, x, y):
        super().__init__("Карфагенский лучник", 65, 17, x, y)

class CarthaginianCavalry(Cavalry):
    def __init__(self, x, y):
        super().__init__("Карфагенский всадник", 110, 24, x, y)
