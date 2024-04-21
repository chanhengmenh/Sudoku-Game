import pygame, sys
from Settings import width, height, cell_size
from Table import Table
from Home import Home
from Database import insert_user, username_exists

pygame.init()

screen = pygame.display.set_mode((width, height + (cell_size[1] * 3)))
pygame.display.set_caption("Sudoku")

pygame.font.init()

class Main:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sudoku Game")
        self.FPS = pygame.time.Clock()
        self.color = pygame.Color("green")
        self.lives_font = pygame.font.SysFont("monospace", cell_size[0] // 2)
        self.message_font = pygame.font.SysFont('Bauhaus 93', (cell_size[0]))



    def main(self):
        home_screen = Home(self.screen)
        username = home_screen.capture_username()
        if username:
            home_screen.main()
            self.start_game()

    def start_game(self):    
        table = Table(self.screen)
        while True:
            #screen field
            self.screen.fill(pygame.Color(0, 191, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Handle mouse click events
                    table.handle_mouse_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    
                    # Assuming you have a method to handle keyboard input in the Table class
                    table.handle_keyboard_input(event.key)

            # lower screen display
            if not table.game_over:
                my_lives = self.lives_font.render(f"Lives Left: {table.lives}", True, pygame.Color("black"))
                self.screen.blit(my_lives, ((width // table.SRN) - (cell_size[0] // 2), height + (cell_size[1] * 2.2)))
            
            else:
                if table.lives <= 0:
                    message = self.message_font.render("GAME OVER!!", True, pygame.Color("red"))
                    self.screen.blit(message, (cell_size[0] + (cell_size[0] // 2), height + (cell_size[1] * 2)))
                elif table.lives > 0:
                    message = self.message_font.render("You Made It!!!", True, self.color)
                    self.screen.blit(message, (cell_size[0] , height + (cell_size[1] * 2)))
            
            table.update()
            pygame.display.flip()
            self.FPS.tick(30)


if __name__ == "__main__":
    game = Main(width, height + (cell_size[1] * 3))
    game.main()
