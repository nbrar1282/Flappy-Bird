import pygame

class Textbox(pygame.sprite.Sprite):
    def __init__(self, dimensions, color, bgcolor, text, font_size=24):
        super().__init__()
        self.dimensions = dimensions
        self.color = color
        self.bgcolor = bgcolor
        self.font_size = font_size

        self._text = text
        self.update()

        self.rect = self.image.get_rect()

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = str(value)
        self.update()

    def create_gradient_surface(self, width, height, color1, color2):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        step = 1 / height
        for y in range(height):
            color = [x + step * (y * (y2 - x)) for x, y2 in zip(color1, color2)]
            pygame.draw.line(surface, color, (0, y), (width, y))
        return surface

    def update(self):
        gradient_surface = self.create_gradient_surface(self.dimensions[0], self.dimensions[1], self.bgcolor, (0, 0, 0))

        font = pygame.font.Font('SamuraiBlast-YznGj.ttf', 30)  # Using a system font
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.dimensions[0] / 2, self.dimensions[1] / 2))

        # Adding shadow
        shadow_color = (0, 0, 0)  # Black shadow
        shadow_surface = font.render(self.text, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
        gradient_surface.blit(shadow_surface, shadow_rect)

        gradient_surface.blit(text_surface, text_rect)
        self.image = gradient_surface
