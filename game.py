import pygame
from screens.welcome_screen import WelcomeScreen
from screens.game import GameScreen
from screens.game_over_screen import GameOverScreen
from config_loader import config  # Import the loaded configuration
from screens.config_screen import ConfigScreen

def main():
    pygame.init()
    pygame.key.set_repeat(400, 400)

    window_width = config['game_settings']['width']
    window_height = config['game_settings']['height']
    window = pygame.display.set_mode((window_width, window_height))

    screens = {
        'welcome': WelcomeScreen,
        'game': GameScreen,
        'game_over': GameOverScreen,
        'config': ConfigScreen
    }

    current_screen = WelcomeScreen(window)  # Start with the WelcomeScreen
    persistent_data = {}  # Initialize persistent data dictionary

    while current_screen.running:
        current_screen.run()
        next_screen = current_screen.next_screen
        if next_screen:
            persistent_data = current_screen.persistent
            current_screen = screens[next_screen](window, persistent_data)
            # current_screen.persistent = persistent_data  # Pass persistent data to the new screen

    pygame.quit()

if __name__ == "__main__":
    main()
