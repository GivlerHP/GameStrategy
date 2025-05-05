# battlefield.py

import pygame
import os
import random

from settings import TILE_SIZE, FIELD_WIDTH, FIELD_HEIGHT, RED, GREEN, BLACK, GRAY, FONT_PATH, FONT_SIZE
SPRITE_DISPLAY_SIZE = 48

# Шрифт для имён и полосок
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)

TEXTURE_PATH = "assets/textures"

# 1) Список файлов-варинтов, но без загрузки картинок
_BACKGROUND_FILES = [
    fname for fname in os.listdir(TEXTURE_PATH)
    if fname.startswith("background") and fname.endswith(".png")
]
# Будет заполнен при первом вызове
_BACKGROUND_TEXTURES = None

# Карта выбранных текстур для каждой клетки
_field_map = None

def _load_background_textures():
    """Ленивая загрузка фоновых текстур после set_mode()"""
    global _BACKGROUND_TEXTURES
    if _BACKGROUND_TEXTURES is None:
        _BACKGROUND_TEXTURES = []
        for fname in _BACKGROUND_FILES:
            path = os.path.join(TEXTURE_PATH, fname)
            # Загрузка с convert_alpha – безопасно после создания окна
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            _BACKGROUND_TEXTURES.append(img)
        # Если ни одного файла не найдено, создаём однотонный
        if not _BACKGROUND_TEXTURES:
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill((180, 180, 180))
            _BACKGROUND_TEXTURES.append(surf)

def draw_field(screen, selected_unit=None, obstacles=None):
    global _field_map
    _load_background_textures()
    # Инициализируем карту фоновых плиток один раз
    if _field_map is None:
        _field_map = [
            [ random.choice(_BACKGROUND_TEXTURES) for _ in range(FIELD_WIDTH) ]
            for __ in range(FIELD_HEIGHT)
        ]

    # 1) Отрисовка фоновых плиток по карте
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            screen.blit(_field_map[y][x], (x * TILE_SIZE, y * TILE_SIZE))

    # 2) Препятствия
    if obstacles:
        for ox, oy in obstacles:
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (ox * TILE_SIZE, oy * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

    # 3) Подсветка доступных клеток для движения
    if selected_unit and selected_unit.can_move():
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                dx = abs(selected_unit.x - x)
                dy = abs(selected_unit.y - y)
                if dx + dy <= selected_unit.movement_points and (x, y) != (selected_unit.x, selected_unit.y):
                    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(
                        surf,
                        (0, 255, 0, 100),
                        (TILE_SIZE // 2, TILE_SIZE // 2),
                        TILE_SIZE // 3
                    )
                    screen.blit(surf, (x * TILE_SIZE, y * TILE_SIZE))

    # 4) Сетка поверх всего
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            rect = pygame.Rect(
                x * TILE_SIZE, y * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(screen, GRAY, rect, 1)


def draw_units(screen, units, color, selected_unit=None):
    for unit in units:
        if not unit.is_alive():
            continue

        x_px = unit.x * TILE_SIZE
        y_px = unit.y * TILE_SIZE
        padding = 10
        unit_rect = pygame.Rect(
            x_px + padding, y_px + padding,
            TILE_SIZE - 2 * padding, TILE_SIZE - 2 * padding
        )

        # Подсветка выбранного юнита
        if unit == selected_unit:
            sel_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(
                sel_surf, (255, 255, 0, 120),
                (TILE_SIZE // 2, TILE_SIZE // 2),
                TILE_SIZE // 3
            )
            screen.blit(sel_surf, (x_px, y_px))

        # Рисуем спрайт или прямоугольник
        sprite_key = unit.__class__.__name__.lower() + ".png"
        sprite_path = os.path.join(TEXTURE_PATH, sprite_key)
        if os.path.exists(sprite_path):
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (SPRITE_DISPLAY_SIZE, SPRITE_DISPLAY_SIZE))
            # Центрируем спрайт в клетке:
            offset = (TILE_SIZE - SPRITE_DISPLAY_SIZE) // 2
            sprite_x = x_px + offset
            sprite_y = y_px + offset
            screen.blit(sprite, (sprite_x, sprite_y))
        else:
            pygame.draw.rect(screen, color, unit_rect)

        # Имя под юнитом
        name_text = FONT.render(unit.name.split()[1], True, BLACK)
        text_rect = name_text.get_rect(
            center=(x_px + TILE_SIZE // 2, y_px + TILE_SIZE - 12)
        )
        screen.blit(name_text, text_rect)

        # Полоска здоровья
        hp_bar_width = TILE_SIZE - 2 * padding
        hp_pct = unit.hp / unit.max_hp
        pygame.draw.rect(
            screen, RED,
            (x_px + padding, y_px + 5, hp_bar_width, 5)
        )
        pygame.draw.rect(
            screen, GREEN,
            (x_px + padding, y_px + 5, hp_bar_width * hp_pct, 5)
        )

