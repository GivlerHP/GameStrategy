# units/carthage.py

import random
from units.carthaginian_units import CarthaginianWarrior, CarthaginianArcher, CarthaginianCavalry
from units.army import Army
from settings import FIELD_WIDTH
from units.unit_factory import UnitFactory

class CarthaginianFactory(UnitFactory):
    def create_warrior(self, x, y):
        return CarthaginianWarrior(x, y)

    def create_archer(self, x, y):
        return CarthaginianArcher(x, y)

    def create_cavalry(self, x, y):
        return CarthaginianCavalry(x, y)

def create_carthage_army():
    factory = CarthaginianFactory()
    x = FIELD_WIDTH - 2

    units = [
        factory.create_warrior(x, 1),
        factory.create_archer(x, 2),
        factory.create_cavalry(x, 3),
    ]

    unit_methods = [factory.create_warrior, factory.create_archer, factory.create_cavalry]
    for i in range(3):
        creator = random.choice(unit_methods)
        y = 4 + i
        units.append(creator(x, y))

    return Army(units)