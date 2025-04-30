# army_factory.py

from abc import ABC, abstractmethod
from units.rome import RomanWarrior, RomanArcher, RomanCavalry
from units.carthage import CarthaginianWarrior, CarthaginianArcher, CarthaginianCavalry

class ArmyFactory(ABC):
    @abstractmethod
    def create_warrior(self, x, y):
        pass

    @abstractmethod
    def create_archer(self, x, y):
        pass

    @abstractmethod
    def create_cavalry(self, x, y):
        pass

class RomeFactory(ArmyFactory):
    def create_warrior(self, x, y):
        return RomanWarrior(x, y)

    def create_archer(self, x, y):
        return RomanArcher(x, y)

    def create_cavalry(self, x, y):
        return RomanCavalry(x, y)

class CarthageFactory(ArmyFactory):
    def create_warrior(self, x, y):
        return CarthaginianWarrior(x, y)

    def create_archer(self, x, y):
        return CarthaginianArcher(x, y)

    def create_cavalry(self, x, y):
        return CarthaginianCavalry(x, y)
