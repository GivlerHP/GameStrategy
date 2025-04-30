# battlefield.py

import pygame
import os
from settings import TILE_SIZE, FIELD_WIDTH, FIELD_HEIGHT, RED, GREEN, BLACK, GRAY, FONT_PATH, FONT_SIZE

FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
TEXTURE_PATH = "assets/textures"

# Загрузка фона
BACKGROUND_IMAGE = pygame.image.load(os.path.join(TEXTURE_PATH, "background.png"))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (TILE_SIZE * FIELD_WIDTH, TILE_SIZE * FIELD_HEIGHT))

# Кэш для спрайтов юнитов
UNIT_SPRITES = {}

SPRITE_SIZE = 52
SPRITE_SOURCE_SIZE = 16

def get_unit_sprite(unit):
    key = unit.__class__.__name__.lower() + ".png"
    if key not in UNIT_SPRITES:
        path = os.path.join(TEXTURE_PATH, key)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
            UNIT_SPRITES[key] = image
        else:
            UNIT_SPRITES[key] = None
    return UNIT_SPRITES[key]

def draw_field(screen, selected_unit=None):
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    if selected_unit and selected_unit.can_move():
        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                dx = abs(selected_unit.x - x)
                dy = abs(selected_unit.y - y)
                if dx + dy <= selected_unit.movement_points and (x != selected_unit.x or y != selected_unit.y):
                    center_x = x * TILE_SIZE + TILE_SIZE // 2
                    center_y = y * TILE_SIZE + TILE_SIZE // 2
                    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(s, (0, 255, 0, 100), (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 3)
                    screen.blit(s, (x * TILE_SIZE, y * TILE_SIZE))

    for x in range(FIELD_WIDTH):
        for y in range(FIELD_HEIGHT):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_units(screen, units, color, selected_unit=None):
    for unit in units:
        if not unit.is_alive():
            continue

        x = unit.x * TILE_SIZE
        y = unit.y * TILE_SIZE
        padding = 10
        rect = pygame.Rect(x + padding, y + padding, TILE_SIZE - 2 * padding, TILE_SIZE - 2 * padding)

        if unit == selected_unit:
            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 0, 120), (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 3)
            screen.blit(s, (x, y))

        sprite = get_unit_sprite(unit)
        if sprite:
            sprite_x = x + TILE_SIZE // 2 - SPRITE_SIZE // 2
            sprite_y = y + TILE_SIZE // 2 - SPRITE_SIZE // 2 - 5
            screen.blit(sprite, (sprite_x, sprite_y))
        else:
            pygame.draw.rect(screen, color, rect)

        name_text = FONT.render(unit.name.split()[1], True, BLACK)
        text_rect = name_text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE - 12))
        screen.blit(name_text, text_rect)

        hp_bar_width = TILE_SIZE - 2 * padding
        hp_percent = unit.hp / unit.max_hp
        pygame.draw.rect(screen, RED, (x + padding, y + 5, hp_bar_width, 5))
        pygame.draw.rect(screen, GREEN, (x + padding, y + 5, hp_bar_width * hp_percent, 5))
