import pygame
import csv
from .base import BaseScreen
from components.bird import Bird  
from components.obstacles import Obstacles
from config_loader import config  
from constants import GAME_OVER, PIPE_KILLED
import os.path

# Define a class for the UI panel that displays game information
class UIPanel:
    def __init__(self, position, size, bgcolor=(0, 0, 0)):
        self.position = position
        self.size = size
        self.bgcolor = bgcolor
        self.font = pygame.font.Font('SamuraiBlast-YznGj.ttf', 24)
        self.elements = {}

    def add_element(self, key, text, position):
        self.elements[key] = {'text': text, 'position': position}

    def update_element(self, key, new_text):
        if key in self.elements:
            self.elements[key]['text'] = new_text

    def draw(self, surface):
        panel_surface = pygame.Surface(self.size)
        panel_surface.fill(self.bgcolor)

        for element in self.elements.values():
            text_surface = self.font.render(element['text'], True, (255, 255, 255))
            panel_surface.blit(text_surface, element['position'])

        surface.blit(panel_surface, self.position)

# Define the main game screen class
class GameScreen(BaseScreen):
    def __init__(self, window, persistent=None):
        super().__init__(window, persistent)
        settings = config['game_settings']

        self.bird = Bird()  # Create an instance of the Bird class
        self.obstacles = Obstacles()  # Create an instance of the Obstacles class
        self.persistent["points"] = self.persistent.get("points", 0)  # Initialize points

        # Create a UI panel to display game information
        self.ui_panel = UIPanel((10, 10), (300, 100), bgcolor=(50, 50, 50))
        self.ui_panel.add_element('score', 'Score: 0', (10, 10))
        self.ui_panel.add_element('lives', 'Lives: 3', (10, 40))
        self.ui_panel.add_element('time', 'Time: 0', (10, 70))
        self.ui_panel.add_element('level', 'Level: 1', (160, 10))

        # Initialize game state variables
        self.level = 1
        self.lives = 3
        self.lost = False
        self.start_time = pygame.time.get_ticks()
        self.level_complete = False
        self.level_complete_message_time = 0
        self.pause_time_update = False

        self.load_level_data()  # Load the level data from a CSV file

    def load_level_data(self):
        try:
            with open(f"levels/level{self.level}.csv") as csvfile:
                self.level_complete = False
                self.start_time = pygame.time.get_ticks()

                reader = csv.reader(csvfile)
                self.obstacles.clear_pipes()
                first_pipe_delay = 500  # Delay for the first pipe

                for row in reader:
                    position, width, height, inverted_str = row
                    position = int(position.strip()) + first_pipe_delay
                    width = int(width.strip())
                    height = int(height.strip())
                    inverted = inverted_str.strip().lower() == 'true'
                    self.obstacles.add_pipe(position, width, height, inverted)

        except FileNotFoundError as e:
            print(e)
            print(f"Level {self.level} not found, ending game.")
            pygame.event.post(pygame.event.Event(GAME_OVER))

    def restart_level(self):
        self.bird.reset_position()
        self.load_level_data()

    def end_game(self, status='killed'):
        self.running = False
        self.next_screen = 'game_over'
        self.persistent['game_status'] = status

    def update(self):
        self.bird.update()
        self.obstacles.update()

        # Check for collision between the bird and the obstacles
        if pygame.sprite.spritecollide(self.bird, self.obstacles, False):
            # Collision logic
            self.lives -= 1
            if self.lives > 0:
                self.restart_level()
            else:
                self.end_game(status='killed')
            return  # Skip updating score and other elements if collision happens

        # Level completion check
        if self.obstacles.all_pipes_cleared() and not self.level_complete:
            self.level_complete = True
            self.level_complete_message_time = pygame.time.get_ticks()
            self.pause_time_update = True

        if self.level_complete and pygame.time.get_ticks() - self.level_complete_message_time > 3000:  # 3 seconds
            next_level = self.level + 1
            next_level_file = f"levels/level{next_level}.csv"

            if os.path.exists(next_level_file):
                self.level = next_level
                self.load_level_data()
                self.pause_time_update = False
            else:
                # Handle the case when there are no more levels
                self.end_game(status='completed')

        # Update game time and score
        current_time = pygame.time.get_ticks()
        if not self.pause_time_update:
            elapsed_time = (current_time - self.start_time) // 1000
            self.ui_panel.update_element('time', f'Time: {elapsed_time}')
        self.ui_panel.update_element('score', f'Score: {self.persistent["points"]}')
        self.ui_panel.update_element('lives', f'Lives: {self.lives}')
        self.ui_panel.update_element('level', f'Level: {self.level}')

    def manage_event(self, event):
        super().manage_event(event)

        if event.type == PIPE_KILLED:
            self.persistent["points"] += 1

        if not self.lost:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.vspeed = -config['game_settings']['jump_boost']

        if event.type == GAME_OVER:
            self.next_screen = 'game_over'
            self.running = False

    def draw(self):
        self.window.fill(config['game_settings']['bg_color'])  # Fill the screen with the background color
        self.window.blit(self.bird.image, self.bird.rect)  # Draw the bird
        self.obstacles.draw(self.window)  # Draw the obstacles
        self.ui_panel.draw(self.window)  # Draw the UI panel

        if self.level_complete:
            level_complete_font = pygame.font.SysFont(None, 36)
            level_complete_message = f"Level {self.level} Complete!"
            message_surface = level_complete_font.render(level_complete_message, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=self.window.get_rect().center)
            self.window.blit(message_surface, message_rect)

        pygame.display.flip()  # Update the display
