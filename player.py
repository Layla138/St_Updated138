import pygame
from constants import WIDTH, HEIGHT

class Player:
    def __init__(self):
        self.character = None
        self.image = None
        self.rect = None

    def set_character(self, character):
        self.character = character

    def start_game(self, assets):
        self.image = assets['character_images'][self.character]
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 5)
