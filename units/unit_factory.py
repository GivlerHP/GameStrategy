# units/unit_factory.py

from abc import ABC, abstractmethod

class UnitFactory(ABC):
    @abstractmethod
    def create_warrior(self, x, y):
        pass

    @abstractmethod
    def create_archer(self, x, y):
        pass

    @abstractmethod
    def create_cavalry(self, x, y):
        pass
