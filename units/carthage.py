# units/carthage.py

from units.base import Warrior, Archer, Cavalry
from settings import FIELD_WIDTH

class CarthaginianWarrior(Warrior):
    def __init__(self, x, y):
        super().__init__("Карфагенский воин", 100, 27, x, y)

class CarthaginianArcher(Archer):
    def __init__(self, x, y):
        super().__init__("Карфагенский лучник", 65, 17, x, y)

class CarthaginianCavalry(Cavalry):
    def __init__(self, x, y):
        super().__init__("Карфагенский всадник", 110, 24, x, y)

def create_carthage_army():
    class Army:
        def __init__(self):
            self.units = [
                CarthaginianWarrior(FIELD_WIDTH - 1, 0),
                CarthaginianArcher(FIELD_WIDTH - 1, 1),
                CarthaginianCavalry(FIELD_WIDTH - 1, 2),
            ]

    return Army()
