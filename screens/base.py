import pygame


class BaseScreen:
    def __init__(self, window, persistent=None):
        self.persistent = {} if persistent is None else persistent
        self.window = window
        self.next_screen = None  # Holds the string identifier of the next screen
        self.running = True  # Start with True to enter the loop

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)  # Frame rate limit to 60 FPS
            self.handle_events()  # Process input events
            self.update()  # Update the state of the screen
            self.draw()  # Draw the screen
            pygame.display.update()  # Update the display

    def handle_events(self):
        for event in pygame.event.get():
            self.manage_event(event)

    def draw(self):
        # This method will be overridden by subclasses
        pass

    def update(self):
        # This method will be overridden by subclasses
        pass

    def manage_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def switch_to_screen(self, screen_name):
        # This method can be called to switch to a different screen
        self.next_screen = screen_name
        self.running = False  # Stop the current screen's loop to allow the switch
