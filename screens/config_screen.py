import pygame
import toml
from .editable_fields.components.editable_group import EditableGroup
from .editable_fields.components.textbox import TextBox
from config_loader import load_config  # Import the load_config function

class ConfigScreen:
    def __init__(self, window, persistent=None):
        # Initialize the configuration screen
        self.window = window
        self.original_size = window.get_size()  # Save the original window size
        self.running = True
        self.next_screen = None
        self.persistent = persistent
        self.config = load_config("config.toml")  # Load current configuration

        # Set a fixed window size for the config screen
        window_width, window_height = 800, 600
        self.window = pygame.display.set_mode((window_width, window_height))

        self.group = EditableGroup()  # Group to manage editable fields
        self.init_text_boxes()  # Initialize the text boxes for settings

        # Button dimensions and positions
        button_width = 120
        button_height = 50
        button_x = window_width - button_width - 50  # Position on the right
        button_y = window_height - 3 * button_height - 30  # Position from bottom

        # Create Save button
        self.save_button = TextBox((button_width, button_height), "Save", id="save_button", bgcolor=(200, 200, 200), font_size=36)
        self.save_button.rect.topleft = (button_x, button_y)

        # Create Default button
        self.default_button = TextBox((button_width, button_height), "Default", id="default_button", bgcolor=(200, 200, 200), font_size=36)
        self.default_button.rect.topleft = (button_x, button_y + button_height + 10)

        # Create Back button
        self.back_button = TextBox((button_width, button_height), "Back", id="back_button", bgcolor=(200, 200, 200), font_size=36)
        self.back_button.rect.topleft = (button_x, button_y + 2 * (button_height + 10))

        # Variables for showing save message
        self.show_save_message = False
        self.message_display_time = 0
    
    def init_text_boxes(self):
        # Initialize text boxes for each setting
        y_offset = 50  # Starting vertical position
        label_width = 150
        value_box_width = 200
        spacing = 20

        # Create a label and text box for each setting
        for key, value in self.config["game_settings"].items():
            # Create label for setting
            label = TextBox((label_width, 50), key, id=f"label_{key}", bgcolor=(200, 200, 200), color=(0, 0, 0))
            label.rect.topleft = (50, y_offset)
            self.group.add(label)

            # Create editable box for setting value
            value_str = str(value) if not isinstance(value, list) else ' '.join(map(str, value))
            box = TextBox((value_box_width, 50), value_str, id=key, bgcolor=(255, 255, 255), color=(0, 0, 0))
            box.rect.topleft = (50 + label_width + spacing, y_offset)
            self.group.add(box)

            y_offset += 70  # Increment vertical position for next setting

    def run(self):
        # Main loop for the configuration screen
        message_font = pygame.font.Font('SamuraiBlast-YznGj.ttf', 22)
        message_text = "Configuration saved. Please restart the game."

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Check if buttons are clicked
                    if self.save_button.rect.collidepoint(event.pos):
                        self.save_config()
                    elif self.default_button.rect.collidepoint(event.pos):
                        self.restore_default_settings()
                    elif self.back_button.rect.collidepoint(event.pos):
                        self.exit_config()
                    self.group.manage_click(event)
                elif event.type == pygame.KEYDOWN:
                    self.group.manage_key(event)

            # Draw interface elements
            self.window.fill((0, 0, 0))
            self.group.draw(self.window)
            self.window.blit(self.save_button.image, self.save_button.rect)
            self.window.blit(self.default_button.image, self.default_button.rect)
            self.window.blit(self.back_button.image, self.back_button.rect)

            # Show save message if needed
            if self.show_save_message:
                overlay_surface = pygame.Surface((600, 100))
                overlay_surface.set_alpha(128)
                overlay_surface.fill((0, 0, 0))
                message_surface = message_font.render(message_text, True, (255, 0, 0))
                message_rect = message_surface.get_rect(center=(300, 50))
                self.window.blit(overlay_surface, ((self.window.get_width() - 600) // 2, 200))
                self.window.blit(message_surface, ((self.window.get_width() - 600) // 2 + message_rect.x, 200 + message_rect.y))

                # Hide message after a delay
                if pygame.time.get_ticks() - self.message_display_time > 5000:
                    self.show_save_message = False
                    self.exit_config()

            pygame.display.flip()  # Update display

    def save_config(self):
        # Save the current configuration to file
        for box in self.group.sprites():
            key = box.id
            value = box.text
            # Convert value to appropriate type
            if value.isdigit():
                value = int(value)
            elif ',' in value or ' ' in value:
                value = [int(v) for v in value.replace(',', ' ').split()]
            # Update configuration dictionary
            if key in self.config["game_settings"]:
                self.config["game_settings"][key] = value

        # Write configuration to file
        with open("config.toml", 'w') as config_file:
            toml.dump(self.config, config_file)
        # Show save message
        self.show_save_message = True
        self.message_display_time = pygame.time.get_ticks()

    def restore_default_settings(self):
        # Restore settings to default values
        self.config = load_config("default.toml")  # Reload default configuration
        # Update text boxes with default values
        for key, value in self.config["game_settings"].items():
            value_str = str(value) if not isinstance(value, list) else ' '.join(map(str, value))
            for box in self.group.sprites():
                if box.id == key:
                    box.text = value_str

    def exit_config(self):
        # Exit the configuration screen
        self.window = pygame.display.set_mode(self.original_size)
        self.running = False
        self.next_screen = 'welcome'
