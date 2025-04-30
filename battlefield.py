# battlefield.py

import pygame
from settings import TILE_SIZE, FIELD_WIDTH, FIELD_HEIGHT, RED, GREEN, BLACK, GRAY, BLUE, FONT_NAME, FONT_SIZE

FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)


def draw_field(screen, selected_unit=None):
    for x in range(FIELD_WIDTH):
        for y in range(FIELD_HEIGHT):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

            # Подсветка возможных клеток перемещения
            if selected_unit and selected_unit.can_move():
                dx = abs(selected_unit.x - x)
                dy = abs(selected_unit.y - y)
                if dx + dy <= selected_unit.movement_points and (x != selected_unit.x or y != selected_unit.y):
                    pygame.draw.rect(screen, (200, 255, 200), rect)


def draw_units(screen, units, color, selected_unit=None):
    for unit in units:
        if not unit.is_alive():
            continue

        x = unit.x * TILE_SIZE
        y = unit.y * TILE_SIZE
        padding = 10
        rect = pygame.Rect(x + padding, y + padding, TILE_SIZE - 2 * padding, TILE_SIZE - 2 * padding)

        # Подсветка выбранного юнита
        if unit == selected_unit:
            pygame.draw.rect(screen, (255, 255, 0), rect.inflate(6, 6))

        pygame.draw.rect(screen, color, rect)

        # Имя юнита
        name_text = FONT.render(unit.name.split()[1], True, BLACK)
        screen.blit(name_text, (x + 5, y + 30))

        # Полоска здоровья
        hp_bar_width = TILE_SIZE - 2 * padding
        hp_percent = unit.hp / unit.max_hp
        pygame.draw.rect(screen, RED, (x + padding, y + 5, hp_bar_width, 5))
        pygame.draw.rect(screen, GREEN, (x + padding, y + 5, hp_bar_width * hp_percent, 5))
