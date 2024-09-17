import pygame
import os
from constants import *

def load_assets():
    assets = {}

    # Load fonts
    assets['title_font'] = pygame.font.Font(FONT_PATH, 36)
    assets['button_font'] = pygame.font.Font(FONT_PATH, 24)

    # Load images
    assets['wallpaper'] = pygame.image.load("location/wallpaper.png")
    assets['wallpaper'] = pygame.transform.scale(assets['wallpaper'], (WIDTH - 40, HEIGHT - 160))

    assets['gloomy_forest'] = pygame.image.load(os.path.join("location", "gloomy_forest_four.png"))
    assets['gloomy_forest'] = pygame.transform.scale(assets['gloomy_forest'], (WIDTH - 40, HEIGHT - 160))

    # Load character images
    assets['character_images'] = {}
    for character in CHARACTERS:
        img_path = os.path.join(CHARACTER_FOLDER, f"{character}.png")
        if os.path.exists(img_path):
            img = pygame.image.load(img_path)
            assets['character_images'][character] = pygame.transform.scale(img, (100, 100))
        else:
            print(f"Warning: Image for {character} not found.")

    return assets
