# game.py — основной игровой цикл

import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, TILE_SIZE, FONT_PATH, FONT_SIZE
from battlefield import draw_field, draw_units
from units.rome import create_rome_army
from units.carthage import create_carthage_army
from units.base import Warrior, Archer, Cavalry
from ai import ai_turn

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 200))
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
font = pygame.font.SysFont(FONT_PATH, FONT_SIZE)


def log(text):
    if len(battle_log) > 10:
        battle_log.pop(0)
    battle_log.append(text)


def reset_units(units):
    for unit in units:
        if unit.is_alive():
            unit.defending = False
            unit.movement_points = 2


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
        big_font = pygame.font.SysFont(FONT_PATH, 40)
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

            if my < SCREEN_HEIGHT:
                if waiting_for_target and selected_unit and selected_action:
                    for enemy in carthage_army.units:
                        if enemy.is_alive() and enemy.x == grid_x and enemy.y == grid_y:
                            dx = abs(grid_x - selected_unit.x)
                            dy = abs(grid_y - selected_unit.y)
                            manhattan = dx + dy

                            success = False
                            if selected_action == "Ближняя атака":
                                if manhattan == 1:
                                    selected_unit.attack(enemy)
                                    log(f"{selected_unit.name} атакует {enemy.name} вблизи")
                                    success = True
                                else:
                                    log(f"{enemy.name} слишком далеко для ближней атаки")
                            elif selected_action == "Дальняя атака":
                                if isinstance(selected_unit, Archer):
                                    if manhattan <= 4:
                                        selected_unit.distant_attack(enemy)
                                        log(f"{selected_unit.name} стреляет по {enemy.name}")
                                        success = True
                                    else:
                                        log(f"Стрела не долетела до {enemy.name}")
                                else:
                                    log(f"{selected_unit.name} не умеет стрелять!")
                            elif selected_action == "Наскок":
                                aligned = (selected_unit.x == enemy.x or selected_unit.y == enemy.y)
                                if not isinstance(selected_unit, Cavalry):
                                    log(f"{selected_unit.name} не умеет делать наскок")
                                elif not aligned:
                                    log(f"{enemy.name} не на прямой линии для наскока")
                                elif manhattan > 3:
                                    log(f"{enemy.name} слишком далеко для наскока")
                                else:
                                    selected_unit.charge_attack(enemy)
                                    log(f"{selected_unit.name} делает наскок на {enemy.name}")
                                    success = True

                            if success:
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
            actions = selected_unit.get_available_actions() + ["Ничего"]
            key_to_index = {
                pygame.K_1: 0,
                pygame.K_2: 1,
                pygame.K_3: 2,
                pygame.K_4: 3
            }
            if event.key in key_to_index and key_to_index[event.key] < len(actions):
                selected_action = actions[key_to_index[event.key]]

                if selected_action == "Защититься":
                    selected_unit.defend()
                    log(f"{selected_unit.name} защищается")
                    selected_unit = None
                    selected_action = None
                    player_turn_done = True
                elif selected_action == "Ничего":
                    log(f"{selected_unit.name} пропускает действие")
                    selected_unit = None
                    selected_action = None
                    player_turn_done = True
                else:
                    waiting_for_target = True

    if player_turn_done:
        round_number += 1
        ai_turn(carthage_army, rome_army, log)
        reset_units(rome_army.units + carthage_army.units)
        selected_unit = None
        selected_action = None
        waiting_for_target = False
        player_turn_done = False

    if selected_unit:
        actions = selected_unit.get_available_actions() + ["Ничего"]
        for idx, action in enumerate(actions):
            text = font.render(f"{idx + 1}. {action}", True, (0, 0, 0))
            screen.blit(text, (10, SCREEN_HEIGHT + 20 + idx * 25))

        if selected_action:
            info = font.render(f"Выбрано: {selected_action}", True, (0, 0, 0))
            screen.blit(info, (10, SCREEN_HEIGHT + 140))

    for i, line in enumerate(battle_log):
        log_text = font.render(line, True, (0, 0, 0))
        screen.blit(log_text, (300, SCREEN_HEIGHT + 20 + i * 20))

    pygame.display.flip()

pygame.quit()
