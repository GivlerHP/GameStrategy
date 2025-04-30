# game.py — основной игровой цикл

import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, TILE_SIZE, FONT_NAME, FONT_SIZE
from battlefield import draw_field, draw_units
from units.rome import create_rome_army
from units.base import Warrior, Archer, Cavalry
from units.carthage import create_carthage_army

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 200))  # увеличим высоту под лог
pygame.display.set_caption("Battle Game")
clock = pygame.time.Clock()

rome_army = create_rome_army()
carthage_army = create_carthage_army()

selected_unit = None
selected_action = None
waiting_for_target = False
player_turn_done = False
battle_log = []
round_number = 1
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)


def log(text):
    if len(battle_log) > 10:
        battle_log.pop(0)
    battle_log.append(text)


def reset_units(units):
    for unit in units:
        if unit.is_alive():
            unit.defending = False
            unit.movement_points = 2


def ai_turn():
    log(f"Раунд {round_number} — ход Карфагена")
    for unit in carthage_army.units:
        if not unit.is_alive():
            continue

        targets = [u for u in rome_army.units if u.is_alive()]
        if not targets:
            return
        target = random.choice(targets)

        dx = abs(target.x - unit.x)
        dy = abs(target.y - unit.y)
        manhattan = dx + dy

        if manhattan == 1:
            unit.attack(target)
            log(f"{unit.name} атакует {target.name} вблизи")
        elif isinstance(unit, Archer) and manhattan <= 4:
            unit.distant_attack(target)
            log(f"{unit.name} стреляет по {target.name}")
        elif isinstance(unit, Cavalry) and (unit.x == target.x or unit.y == target.y) and manhattan <= 3:
            unit.charge_attack(target)
            log(f"{unit.name} делает наскок на {target.name}")
        else:
            if unit.can_move():
                step_x = 1 if target.x > unit.x else -1 if target.x < unit.x else 0
                step_y = 1 if target.y > unit.y else -1 if target.y < unit.y else 0
                new_x = unit.x + step_x
                new_y = unit.y + step_y

                occupied = any(u.is_alive() and u.x == new_x and u.y == new_y for u in rome_army.units + carthage_army.units)
                if not occupied:
                    unit.move(new_x, new_y)
                    log(f"{unit.name} передвигается")


def check_victory():
    rome_alive = any(u.is_alive() for u in rome_army.units)
    carthage_alive = any(u.is_alive() for u in carthage_army.units)
    if not rome_alive:
        return "Поражение! Карфаген победил."
    if not carthage_alive:
        return "Победа! Рим выиграл."
    return None


running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    draw_field(screen, selected_unit)
    draw_units(screen, rome_army.units, (0, 0, 255), selected_unit)
    draw_units(screen, carthage_army.units, (255, 0, 0))

    victory_message = check_victory()
    if victory_message:
        big_font = pygame.font.SysFont(FONT_NAME, 40)
        text = big_font.render(victory_message, True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x, grid_y = mx // TILE_SIZE, my // TILE_SIZE

            if my < SCREEN_HEIGHT:  # Только клики по полю!
                if waiting_for_target and selected_unit and selected_action:
                    for enemy in carthage_army.units:
                        if enemy.is_alive() and enemy.x == grid_x and enemy.y == grid_y:
                            dx = abs(grid_x - selected_unit.x)
                            dy = abs(grid_y - selected_unit.y)
                            manhattan = dx + dy

                            if selected_action == "Ближняя атака" and manhattan == 1:
                                selected_unit.attack(enemy)
                                log(f"{selected_unit.name} атакует {enemy.name} вблизи")
                                player_turn_done = True
                            elif selected_action == "Дальняя атака" and manhattan <= 4:
                                selected_unit.distant_attack(enemy)
                                log(f"{selected_unit.name} стреляет по {enemy.name}")
                                player_turn_done = True
                            elif selected_action == "Наскок":
                                aligned = (selected_unit.x == enemy.x or selected_unit.y == enemy.y)
                                if aligned and manhattan <= 3:
                                    selected_unit.charge_attack(enemy)
                                    log(f"{selected_unit.name} делает наскок на {enemy.name}")
                                    player_turn_done = True

                            selected_action = None
                            selected_unit = None
                            waiting_for_target = False
                            break

                elif selected_unit and selected_unit.can_move():
                    dx = abs(grid_x - selected_unit.x)
                    dy = abs(grid_y - selected_unit.y)
                    if dx + dy <= selected_unit.movement_points:
                        occupied = any(u.is_alive() and u.x == grid_x and u.y == grid_y for u in rome_army.units + carthage_army.units)
                        if not occupied:
                            selected_unit.move(grid_x, grid_y)
                            log(f"{selected_unit.name} перемещается")

                for unit in rome_army.units:
                    if unit.is_alive() and unit.x == grid_x and unit.y == grid_y:
                        selected_unit = unit
                        selected_action = None
                        waiting_for_target = False

        if event.type == pygame.KEYDOWN and selected_unit and not waiting_for_target:
            actions = selected_unit.get_available_actions()
            key_to_index = {
                pygame.K_1: 0,
                pygame.K_2: 1,
                pygame.K_3: 2
            }
            if event.key in key_to_index and key_to_index[event.key] < len(actions):
                selected_action = actions[key_to_index[event.key]]

                if selected_action == "Защититься":
                    selected_unit.defend()
                    log(f"{selected_unit.name} защищается")
                    selected_unit = None
                    selected_action = None
                    player_turn_done = True
                else:
                    waiting_for_target = True

    if player_turn_done:
        round_number += 1
        ai_turn()
        reset_units(rome_army.units + carthage_army.units)
        selected_unit = None
        selected_action = None
        waiting_for_target = False
        player_turn_done = False

    # Отображение команд юнита
    if selected_unit:
        actions = selected_unit.get_available_actions()
        for idx, action in enumerate(actions):
            text = font.render(f"{idx + 1}. {action}", True, (0, 0, 0))
            screen.blit(text, (10, SCREEN_HEIGHT + 20 + idx * 25))

        if selected_action:
            info = font.render(f"Выбрано: {selected_action}", True, (0, 0, 0))
            screen.blit(info, (10, SCREEN_HEIGHT + 120))

    # Вывод логов снизу
    for i, line in enumerate(battle_log):
        log_text = font.render(line, True, (0, 0, 0))
        screen.blit(log_text, (300, SCREEN_HEIGHT + 20 + i * 20))

    pygame.display.flip()

pygame.quit()
