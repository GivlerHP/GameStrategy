import pygame
import random
import os

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    WHITE, TILE_SIZE, FONT_PATH, FONT_SIZE, GREEN, RED
)
from battlefield import draw_field, draw_units
from units.rome import create_rome_army
from units.carthage import create_carthage_army
from units.base import Warrior, Archer, Cavalry
from ai import ai_turn
from sound import play_sound

pygame.init()

# Фоновая музыка
MUSIC_PATH = os.path.join("assets", "sounds", "battle_theme.mp3")
if os.path.exists(MUSIC_PATH):
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# Окно с дополнительной панелью внизу
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 300))
pygame.display.set_caption("Echo of Great Battles")
clock = pygame.time.Clock()

# Армии
rome_army = create_rome_army()
carthage_army = create_carthage_army()

# Препятствия
NUM_OBSTACLES = 7
obstacles = set()
while len(obstacles) < NUM_OBSTACLES:
    x = random.randint(2, SCREEN_WIDTH // TILE_SIZE - 3)
    y = random.randint(0, SCREEN_HEIGHT // TILE_SIZE - 3)
    if not any(u.x == x and u.y == y for u in rome_army.units + carthage_army.units):
        obstacles.add((x, y))

# Состояние хода
selected_unit = None
selected_action = None
waiting_for_target = False
player_turn_done = False
battle_log = []
round_number = 1
font = pygame.font.Font(FONT_PATH, FONT_SIZE)


def log(text):
    if len(battle_log) > 10:
        battle_log.pop(0)
    battle_log.append(text)


def reset_units(units):
    for u in units:
        if u.is_alive():
            u.defending = False
            u.movement_points = 2


def check_victory():
    if not any(u.is_alive() for u in rome_army.units):
        return "Поражение! Карфаген победил."
    if not any(u.is_alive() for u in carthage_army.units):
        return "Победа! Рим выиграл."
    return None


# === ГЛАВНЫЙ ЦИКЛ ===
running = True
while running:
    clock.tick(FPS)

    # 1) Фон игрового поля (только плитками)
    draw_field(screen, selected_unit, obstacles)

    # 2) Юниты
    draw_units(screen, rome_army.units, (0, 0, 255), selected_unit)
    draw_units(screen, carthage_army.units, (255, 0, 0))

    # 3) Нижняя панель — заливаем перед текстом
    pygame.draw.rect(
        screen,
        (240, 240, 240),
        (0, SCREEN_HEIGHT, SCREEN_WIDTH, 300)
    )

    # 4) Проверка победы
    victory = check_victory()
    if victory:
        big_font = pygame.font.Font(FONT_PATH, 72)

        if victory.startswith("Победа"):
            color = GREEN
        elif victory.startswith("Поражение"):
            color = RED
        else:
            color = WHITE  # на всякий случай, если текст будет другой

        txt = big_font.render(victory, True, color)
        screen.blit(
            txt,
            (SCREEN_WIDTH // 2 - txt.get_width() // 2,
             SCREEN_HEIGHT // 2 - txt.get_height() // 2)
        )
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    # 6) События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Клик по полю
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // TILE_SIZE, my // TILE_SIZE

            # Только если не на панели
            if my < SCREEN_HEIGHT:
                # Целевой режим (атака)
                if waiting_for_target and selected_unit and selected_action:
                    for enemy in carthage_army.units:
                        if enemy.is_alive() and (enemy.x, enemy.y) == (gx, gy):
                            dx, dy = abs(gx - selected_unit.x), abs(gy - selected_unit.y)
                            manh = dx + dy
                            ok = False

                            if selected_action == "Ближняя атака":
                                if manh == 1:
                                    selected_unit.attack(enemy)
                                    log(f"{selected_unit.name} атакует {enemy.name} вблизи")
                                    ok = True
                                else:
                                    log(f"{enemy.name} слишком далеко для ближней атаки")

                            elif selected_action == "Дальняя атака":
                                if isinstance(selected_unit, Archer):
                                    if manh <= 4:
                                        selected_unit.distant_attack(enemy)
                                        log(f"{selected_unit.name} стреляет по {enemy.name}")
                                        ok = True
                                    else:
                                        log(f"Стрела не долетела до {enemy.name}")
                                else:
                                    log(f"{selected_unit.name} не умеет стрелять!")

                            elif selected_action == "Наскок":
                                aligned = (selected_unit.x == gx or selected_unit.y == gy)
                                if not isinstance(selected_unit, Cavalry):
                                    log(f"{selected_unit.name} не умеет делать наскок")
                                elif not aligned:
                                    log(f"{enemy.name} не на прямой линии для наскока")
                                elif manh > 3:
                                    log(f"{enemy.name} слишком далеко для наскока")
                                else:
                                    selected_unit.charge_attack(enemy)
                                    log(f"{selected_unit.name} делает наскок на {enemy.name}")
                                    ok = True

                            if ok:
                                player_turn_done = True

                            selected_unit = None
                            selected_action = None
                            waiting_for_target = False
                            break

                # Перемещение
                elif selected_unit and selected_unit.can_move():
                    dx, dy = abs(gx - selected_unit.x), abs(gy - selected_unit.y)
                    if dx + dy <= selected_unit.movement_points:
                        occ = any(u.is_alive() and (u.x, u.y) == (gx, gy)
                                  for u in rome_army.units + carthage_army.units)
                        if not occ and (gx, gy) not in obstacles:
                            selected_unit.move(gx, gy)
                            log(f"{selected_unit.name} перемещается")

                # Выбор юнита
                else:
                    for u in rome_army.units:
                        if u.is_alive() and (u.x, u.y) == (gx, gy):
                            selected_unit = u
                            selected_action = None
                            waiting_for_target = False
                            break

        # Клавиши для выбора приёма
        elif event.type == pygame.KEYDOWN and selected_unit and not waiting_for_target:
            acts = selected_unit.get_available_actions() + ["Ничего"]
            mapping = {pygame.K_1: 0, pygame.K_2: 1,
                       pygame.K_3: 2, pygame.K_4: 3}
            if event.key in mapping and mapping[event.key] < len(acts):
                selected_action = acts[mapping[event.key]]

                if selected_action == "Защититься":
                    selected_unit.defend()
                    log(f"{selected_unit.name} защищается")
                    player_turn_done = True
                    selected_unit = None
                    selected_action = None

                elif selected_action == "Ничего":
                    log(f"{selected_unit.name} пропускает действие")
                    player_turn_done = True
                    selected_unit = None
                    selected_action = None

                else:
                    waiting_for_target = True

    # 7) Когда игрок ходы сделал
    if player_turn_done:
        round_number += 1
        ai_turn(carthage_army, rome_army, log, obstacles)
        reset_units(rome_army.units + carthage_army.units)
        player_turn_done = False

    # 8) Интерфейс — слева список приёмов
    if selected_unit:
        acts = selected_unit.get_available_actions() + ["Ничего"]
        for i, act in enumerate(acts):
            txt = font.render(f"{i+1}. {act}", True, (0, 0, 0))
            screen.blit(txt, (10, SCREEN_HEIGHT + 20 + i*30))

        if selected_action:
            info = font.render(f"Выбрано: {selected_action}", True, (0, 0, 0))
            screen.blit(info, (10, SCREEN_HEIGHT + 150))

    # 9) Интерфейс — справа лог
    for i, line in enumerate(battle_log):
        txt = font.render(line, True, (0, 0, 0))
        screen.blit(txt, (SCREEN_WIDTH//2, SCREEN_HEIGHT + 20 + i*25))

    pygame.display.flip()

pygame.quit()
