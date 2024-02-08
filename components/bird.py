import pygame
from config_loader import config  # Import the configuration

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        bird_settings = config.get('game_settings', {})

        self.max_vspeed = bird_settings.get('max_vspeed', 5)
        self.start_position_bottom = bird_settings.get('start_position_bottom', 100)

        self.image = pygame.transform.scale(pygame.image.load("images/bird.png"), (100, 100)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = self.start_position_bottom
        self.vspeed = 0

    def update(self):
        self.vspeed = min(self.max_vspeed, self.vspeed + 1)
        self.rect.y += self.vspeed

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.rect.bottom = pygame.display.get_surface().get_height()
            self.vspeed = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.vspeed = 0

    def reset_position(self):
        self.rect.bottom = self.start_position_bottom
        self.vspeed = 0
