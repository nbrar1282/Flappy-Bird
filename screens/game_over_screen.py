
import pygame
from .base import BaseScreen
from components.textbox import Textbox
from config_loader import config  # Import the configuration

class GameOverScreen(BaseScreen):
    def __init__(self, window, persistent=None):
        super().__init__(window, persistent)
        self.init_ui()

    def init_ui(self):
        score_text = f"Final Score: {self.persistent.get('score', 0)}"
        self.score_textbox = Textbox((600, 50), (255, 255, 255), (0, 0, 0), score_text, font_size=30)
        self.score_textbox.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2 - 50)

       
        
        self.restart_button = Button((300, 50, 200, 50), "Restart", font_size=30)
        self.restart_button.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2 + 100)

        score_text = f"Final Score: {self.persistent.get('points', 0)}"
        self.score_textbox = Textbox((400, 50), (255, 255, 255), (0, 0, 0), score_text, font_size=30)
        self.score_textbox.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2 - 50)

        self.quit_button = Button((300, 50, 200, 50), "Quit", font_size=30)
        self.quit_button.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2 + 160)

       
        

        status_text = f" {'You were killed' if self.persistent.get('game_status') == 'killed' else 'You have completed all the levels'}!"
        self.status_textbox = Textbox((600, 50), (255, 255, 255), (0, 0, 0), status_text, font_size=30)
        self.status_textbox.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2 - 100)


    def manage_event(self, event):
        super().manage_event(event)
        if self.restart_button.is_clicked(event):
            self.persistent = {}
            self.switch_to_screen('game')
        elif self.quit_button.is_clicked(event):
            self.running = False
        

    def update(self):
        self.restart_button.update(pygame.mouse.get_pos())
        self.quit_button.update(pygame.mouse.get_pos())
        


    def draw(self):
        self.window.fill(config['game_settings']['bg_color'])
        self.window.blit(self.score_textbox.image, self.score_textbox.rect)

        
        self.restart_button.draw(self.window)
        self.quit_button.draw(self.window)
        self.window.blit(self.status_textbox.image, self.status_textbox.rect)




class Button:
    def __init__(self, rect, text, font_size=30, text_color=(255, 255, 255), bg_color=(0, 0, 0), hover_color=(100, 100, 100)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.font = pygame.font.Font('SamuraiBlast-YznGj.ttf', font_size)
        self.hovered = False

    def draw(self, surface):
        bg_color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return self.hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
