# units/rome.py

from units.base import Warrior, Archer, Cavalry

class RomanWarrior(Warrior):
    def __init__(self, x, y):
        super().__init__("Римский воин", 100, 25, x, y)

class RomanArcher(Archer):
    def __init__(self, x, y):
        super().__init__("Римский лучник", 70, 15, x, y)

class RomanCavalry(Cavalry):
    def __init__(self, x, y):
        super().__init__("Римский всадник", 120, 20, x, y)

def create_rome_army():
    class Army:
        def __init__(self):
            self.units = [
                RomanWarrior(0, 0),
                RomanArcher(0, 1),
                RomanCavalry(0, 2),
            ]

    return Army()
