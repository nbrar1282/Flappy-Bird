import pygame
from .textbox import TextBox

class EditableGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def manage_click(self, event):
        for s in self.sprites():
            s.selected = False
            if s.rect.collidepoint(event.pos):
                s.selected = True
            if s.selected:
                if isinstance(s, TextBox):  # Check if the sprite is a TextBox
                    s.handle_key_input(event)

    def manage_key(self, event):
        for s in self.sprites():
            if s.selected and isinstance(s, TextBox):
                s.handle_key_input(event)

    
