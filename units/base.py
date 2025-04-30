# units/base.py

from abc import ABC, abstractmethod

class Unit(ABC):
    def __init__(self, name, hp, damage, x, y):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
        self.x = x
        self.y = y
        self.defending = False
        self.movement_points = 2

    def is_alive(self):
        return self.hp > 0

    def can_move(self):
        return self.movement_points > 0

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.movement_points -= 1

    def reset_turn(self):
        self.defending = False
        self.movement_points = 2

    def take_damage(self, amount):
        if self.defending:
            amount //= 2
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def attack(self, target):
        target.take_damage(self.damage)

    def defend(self):
        self.defending = True

    def distant_attack(self, target):
        target.take_damage(self.damage + 10)

    def charge_attack(self, target):
        target.take_damage(self.damage + 20)

    @abstractmethod
    def get_available_actions(self):
        pass

class Warrior(Unit):
    def get_available_actions(self):
        return ["Ближняя атака", "Защититься"]

class Archer(Unit):
    def get_available_actions(self):
        return ["Ближняя атака", "Дальняя атака"]

class Cavalry(Unit):
    def get_available_actions(self):
        return ["Ближняя атака", "Наскок"]
