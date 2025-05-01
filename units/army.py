# units/army.py

class Army:
    def __init__(self, units):
        self.units = units

    def is_defeated(self):
        return all(not unit.is_alive() for unit in self.units)

    def get_alive_units(self):
        return [unit for unit in self.units if unit.is_alive()]
