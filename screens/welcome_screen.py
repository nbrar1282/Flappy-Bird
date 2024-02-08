import pygame
from .base import BaseScreen
from components.textbox import Textbox
from config_loader import config  # Import the configuration

class WelcomeScreen(BaseScreen):
    def __init__(self, window, persistent=None):
        super().__init__(window, persistent)
        self.init_ui()

    def init_ui(self):
        name_text = "Navdeep Singh Brar"  
        student_id_text = "Student ID: A01359046"  
        self.name_textbox = Textbox((400, 70), (255, 255, 255), (0, 0, 0), name_text, font_size=24) # Create a textbox for the name
        self.student_id_textbox = Textbox((400, 50), (255, 255, 255), (0, 0, 0), student_id_text, font_size=24) # Create a textbox for the student ID

        # Position the textboxes
        self.name_textbox.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2 - 100)
        self.student_id_textbox.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2 - 50)

        self.start_button = Button((200, 50, 200, 50), "Start Game", font_size=30)
        self.start_button.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2)

        # Add a button for navigating to the ConfigScreen
        self.config_button = Button((200, 50, 200, 50), "Settings", font_size=30)
        self.config_button.rect.center = (self.window.get_width() // 2, self.window.get_height() // 2 + 100)

        self.background = pygame.image.load('images/welcomebg.png')

    def manage_event(self, event):
        super().manage_event(event)
        if self.start_button.is_clicked(event):
            self.switch_to_screen('game') # Switch to the game screen
        elif self.config_button.is_clicked(event):
            self.switch_to_screen('config')

    def update(self):
        self.start_button.update(pygame.mouse.get_pos())
        self.config_button.update(pygame.mouse.get_pos())  # Update the new button


    def draw(self):
        self.window.fill(config['game_settings']['bg_color'])
        self.window.blit(self.name_textbox.image, self.name_textbox.rect)
        self.window.blit(self.student_id_textbox.image, self.student_id_textbox.rect)
        self.start_button.draw(self.window)
        self.config_button.draw(self.window)  # Draw the new button

class Button:
    def __init__(self, rect, text, font_size=30, text_color=(255, 255, 255), bg_color=(0, 0, 0), hover_color=(100, 100, 100)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.font = pygame.font.Font('SamuraiBlast-YznGj.ttf', font_size) # Create a font for the button
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
