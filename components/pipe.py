import pygame
from config_loader import config  # Import the configuration
from constants import BIRD_CLEARED_PIPE, PIPE_KILLED

class Pipe(pygame.sprite.Sprite):
    def __init__(self, position, width, height, inverted=False):
        super().__init__()

        # Use configuration values or defaults
        self.pipe_speed = config['game_settings']['speed']
        self.pipe_color = config['game_settings']['pipe_color']
        self.pipe_height = config['game_settings']['height']

        # Set the width and height of the pipe based on parameters
        self.image = pygame.surface.Surface((width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.fill(self.pipe_color)
        self.rect = self.image.get_rect()

        if inverted:
            self.rect.top = 0
        else:
            self.rect.bottom = self.pipe_height

        self.rect.left = position

    def update(self):
        self.rect.x -= self.pipe_speed
        if self.rect.right < 0:
            self.kill()
            pygame.event.post(pygame.event.Event(BIRD_CLEARED_PIPE))
            pygame.event.post(pygame.event.Event(PIPE_KILLED))
