import pygame
from .pipe import Pipe
from config_loader import config  # Import the configuration

class Obstacles(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        

    def update(self, *args, **kwargs):
        # Since pipes are now loaded from CSV, we remove the random generation logic
        return super().update(*args, **kwargs)

    def add_pipe(self, position, width, height, inverted):
        # Add a new pipe based on the specified parameters
        new_pipe = Pipe(position, width, height, inverted)
        self.add(new_pipe)

    def all_pipes_cleared(self):
        # Check if all pipes have been cleared (off-screen)
        for pipe in self.sprites():
            if pipe.rect.right > 0:  # If any pipe is still on screen
                return False
        return True

    def clear_pipes(self):
        # Remove all pipes from the group
        self.empty()

    @property
    def rightmost_pipe(self):
        # This might not be needed anymore depending on your new level design
        return max((s.rect.right for s in self.sprites()), default=0)
