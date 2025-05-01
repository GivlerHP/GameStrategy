# sound.py — загрузка и воспроизведение звуков

import pygame
import os

SOUND_PATH = "assets/sounds"

# Предзагрузка звуков (используем mp3 вместо wav)
SOUNDS = {
  # "attack": pygame.mixer.Sound(os.path.join(SOUND_PATH, "attack.mp3")),
 #   "defend": pygame.mixer.Sound(os.path.join(SOUND_PATH, "defend.mp3")),
 #   "death": pygame.mixer.Sound(os.path.join(SOUND_PATH, "death.mp3")),
}

# Настройка громкости (от 0.0 до 1.0)
for sound in SOUNDS.values():
    sound.set_volume(0.5)

def play_sound(name):
    sound = SOUNDS.get(name)
    if sound:
        sound.play()