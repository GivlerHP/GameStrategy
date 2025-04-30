import pygame

# Инициализация Pygame
pygame.init()

# Размер клетки
TILE_SIZE = 110

# Размер поля
FIELD_WIDTH = 12
FIELD_HEIGHT = 6

# Размер экрана
SCREEN_WIDTH = TILE_SIZE * FIELD_WIDTH
SCREEN_HEIGHT = TILE_SIZE * FIELD_HEIGHT + 100

# Частота кадров
FPS = 30

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (180, 180, 180)

# Шрифт по умолчанию
FONT_PATH = "assets/fonts/pixel.ttf"
FONT_SIZE = 27