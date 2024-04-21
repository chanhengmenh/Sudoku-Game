import pygame, sys
import re
from Database import insert_user

# Define the screen dimensions
width, height = 450, 600

FPS = 60 # Frame Per Second

dark_navi_color = pygame.Color(0, 0, 128)
dark_gold_color = pygame.Color(139, 101, 0) # Dark gold

class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, pygame.Color('black'))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print("Enter key pressed.")
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    print("Text changed:", self.text) # Print message when text is changed
                else:
                    self.text += event.unicode
                    print("Text added:", self.text) # Print message when text is added
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, pygame.Color('black'))

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class Button:
    def __init__(self, screen, text, x, y, width, height, font, color, callback=None):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.text_surface = self.font.render(self.text, True, "yellow")
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_click(self):
        if self.callback:
            self.callback()

class Home:
    def __init__(self, screen):
        self.screen = screen
        self.start_button_clicked = False
        self.font = pygame.font.SysFont('Bauhaus 93', 60)
        self.button_font = pygame.font.SysFont('Bauhaus 93', 40)
        
        # the identify input box
        self.name_box = InputBox(width // 2 - 150, 2 * height // 3 - 100, 300, 50)
        
        # Initialize buttons
        self.start_button = Button(self.screen, "START", width // 2 - 50 - 150, 4 * height // 5, 150, 60, self.button_font, "red", callback=self.start_game)
        self.exit_button = Button(self.screen, "EXIT", width // 2 + 50, 4 * height // 5, 150, 60, self.button_font, "red", callback=self.exit_game)
        
        # Render the text
        self.text = "Sudoku Game!"
        self.text_surface = self.font.render(self.text, True, pygame.Color(dark_gold_color))

    def draw(self, screen): # Modify this line to accept screen as a parameter
        self.screen.fill(dark_navi_color) # Fill the screen with a background color
        self.name_box.draw(self.screen) # Draw the name input box
        self.start_button.draw(self.screen) # Draw the start button
        self.exit_button.draw(self.screen) # Draw the exit button
        # Draw the text surface on the screen at the specified location
        screen.blit(self.text_surface, (width // 2 - 190, height // 4))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            self.name_box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if self.start_button.is_clicked(event.pos):
                    self.start_button_clicked = True

        #         elif self.exit_button.is_clicked(event.pos):
        #             self.exit_button.handle_click()
        # return None
    
    def start_game(self):
        if self.name_box.text:
            print(f"User name: {self.name_box.text}")
            print("Starting the game...")
            # Add the logic to start the game here
        else:
            print("User information not provided.")

    def exit_game(self):
        print("Exiting the game...")
        pygame.quit()
        sys.exit()

    def capture_username(self):
        # This method should capture the username from the GUI
        # and return it. This is a placeholder implementation.
        username = "example_username" # Replace this with actual GUI input capture
        return username

    def start_game_triggered(self):
        # This method should return True if the "Start" button was clicked
        # You might need to implement logic to track the button click state
        return self.start_button_clicked # Assuming you have a way to track this state

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.name_box.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    if self.start_button.is_clicked(event.pos):
                        self.start_button.handle_click()
                    elif self.exit_button.is_clicked(event.pos):
                        self.exit_button.handle_click()

            # Draw everything
            self.draw(self.screen)
            pygame.display.flip()

        # Optionally, perform any cleanup or setup for the game here


