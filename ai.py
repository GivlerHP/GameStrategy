# ai.py — логика ИИ Карфагена (тактическая версия)

from units.base import Archer, Cavalry, Warrior

def ai_turn(carthage_army, rome_army, log):
    log("Ход Карфагена")
    for unit in carthage_army.units:
        if not unit.is_alive():
            continue

        targets = [u for u in rome_army.units if u.is_alive()]
        if not targets:
            return

        target = min(targets, key=lambda u: abs(u.x - unit.x) + abs(u.y - unit.y))
        dx = target.x - unit.x
        dy = target.y - unit.y
        manhattan = abs(dx) + abs(dy)

        # --- ВОИН ---
        if isinstance(unit, Warrior):
            if manhattan == 1:
                unit.attack(target)
                log(f"{unit.name} атакует {target.name} вблизи")
            elif unit.can_move():
                step_x = 1 if dx > 0 else -1 if dx < 0 else 0
                step_y = 1 if dy > 0 else -1 if dy < 0 else 0
                try_move(unit, step_x, step_y, carthage_army.units, rome_army.units, log)

        # --- ЛУЧНИК ---
        elif isinstance(unit, Archer):
            if manhattan <= 4:
                unit.distant_attack(target)
                log(f"{unit.name} стреляет по {target.name}")
            elif unit.can_move():
                if manhattan <= 2:
                    step_x = -1 if dx > 0 else 1 if dx < 0 else 0
                    step_y = -1 if dy > 0 else 1 if dy < 0 else 0
                else:
                    step_x = 1 if dx > 0 else -1 if dx < 0 else 0
                    step_y = 1 if dy > 0 else -1 if dy < 0 else 0
                try_move(unit, step_x, step_y, carthage_army.units, rome_army.units, log)

        # --- ВСАДНИК ---
        elif isinstance(unit, Cavalry):
            same_line = (unit.x == target.x or unit.y == target.y)
            if same_line and 1 < manhattan <= 3:
                unit.charge_attack(target)
                log(f"{unit.name} делает наскок на {target.name}")
            elif unit.can_move():
                if unit.x != target.x:
                    step_x = 1 if dx > 0 else -1
                    step_y = 0
                else:
                    step_x = 0
                    step_y = 1 if dy > 0 else -1
                try_move(unit, step_x, step_y, carthage_army.units, rome_army.units, log)


def try_move(unit, step_x, step_y, allies, enemies, log):
    new_x = unit.x + step_x
    new_y = unit.y + step_y
    occupied = any(
        u.is_alive() and u.x == new_x and u.y == new_y
        for u in allies + enemies
    )
    if not occupied:
        unit.move(new_x, new_y)
        log(f"{unit.name} перемещается")
