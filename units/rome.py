# units/rome.py

import random
from units.rome_units import RomanWarrior, RomanArcher, RomanCavalry
from units.army import Army
from settings import FIELD_WIDTH
from units.unit_factory import UnitFactory

class RomanFactory(UnitFactory):
    def create_warrior(self, x, y):
        return RomanWarrior(x, y)

    def create_archer(self, x, y):
        return RomanArcher(x, y)

    def create_cavalry(self, x, y):
        return RomanCavalry(x, y)

def create_rome_army():
    factory = RomanFactory()
    units = [
        factory.create_warrior(1, 1),
        factory.create_archer(1, 2),
        factory.create_cavalry(1, 3),
    ]

    unit_methods = [factory.create_warrior, factory.create_archer, factory.create_cavalry]
    for i in range(3):
        creator = random.choice(unit_methods)
        y = 4 + i
        units.append(creator(1, y))

    return Army(units)
