# units/rome_units.py

from units.base import Warrior, Archer, Cavalry

class RomanWarrior(Warrior):
    def __init__(self, x, y):
        super().__init__("Римский воин", 100, 25, x, y)

class RomanArcher(Archer):
    def __init__(self, x, y):
        super().__init__("Римский лучник", 70, 15, x, y)

class RomanCavalry(Cavalry):
    def __init__(self, x, y):
        super().__init__("Римский всадник", 110, 22, x, y)