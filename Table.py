import pygame
# import math
from Cell import Cell
from Sudoku import Sudoku
from Clock import Clock
from Settings import width, height, num_cell, cell_size

pygame.font.init()

class Table:
    def __init__(self, screen):
        self.screen = screen
        self.puzzle = Sudoku(num_cell, (num_cell * num_cell) // 2)
        self.clock = Clock()
        self.answers = self.puzzle.puzzle_answers()
        self.answerable_table = self.puzzle.puzzle_table()
        #SRN = Square Root of N
        self.SRN = self.puzzle.SRN #N is the size of side of the Sudoku Square
        self.table_cells = []
        self.clicked_cell = None
        self.clicked_num_below = None
        self.cell_to_empty = None
        self.making_move = False
        self.guess_mode = True
        self.lives = 1000
        self.game_over = False
        self.delete_button = pygame.Rect(0, (height + cell_size[1]), (cell_size[0] * 3), (cell_size[1]))
        self.guess_button = pygame.Rect((cell_size[0] * 6), (height + cell_size[1]), (cell_size[0] * 3), (cell_size[1]))
        self.font = pygame.font.SysFont('Bauhaus 93', (cell_size[0] // 2))
        self.font_color = pygame.Color("white")
        self._generate_game()
        self.clock.start_timer()

    def _generate_game(self):
        # generating sudoku table
        for y in range(num_cell):
            for x in range(num_cell):
                cell_value = self.answerable_table[y][x]
                is_correct_guess = True if cell_value != 0 else False
                self.table_cells.append(Cell(x, y, cell_size, cell_value, is_correct_guess))
    
    def _draw_grid(self):
        grid_color = (50, 80, 80)
        pygame.draw.rect(self.screen, grid_color, (-3, -3, width + 6, height + 6), 6)
        i = 1
        while (i * cell_size[0]) < width:
            line_size = 2 if i % 3 > 0 else 4
            pygame.draw.line(self.screen, grid_color, ((i * cell_size[0]) - (line_size // 2), 0), ((i * cell_size[0]) - (line_size // 2), height), line_size)
            pygame.draw.line(self.screen, grid_color, (0, (i * cell_size[0]) - (line_size // 2)), (height, (i * cell_size[0]) - (line_size // 2)), line_size)
            i += 1

    def _draw_buttons(self):
        # adding "Delete" button details
        dl_button_color = pygame.Color(153, 101, 21)         #dark_gold_color = pygame.Color(153, 101, 21)
        pygame.draw.rect(self.screen, dl_button_color, self.delete_button)
        del_msg = self.font.render("Delete", True, self.font_color)
        self.screen.blit(del_msg, (self.delete_button.x + (cell_size[0] // 2), self.delete_button.y + (cell_size[1] // 4)))
       
        # adding "Guess On" button details
        gss_button_color = pygame.Color(153, 101, 21) if self.guess_mode else pygame.Color("purple")
        pygame.draw.rect(self.screen, gss_button_color, self.guess_button)
        gss_msg = self.font.render("Guess: On" if self.guess_mode else "Guess: Off", True, self.font_color)
        self.screen.blit(gss_msg, (self.guess_button.x + (cell_size[0] // 3), self.guess_button.y + (cell_size[1] // 4)))
    
    def _get_cell_from_pos(self, pos):
        for cell in self.table_cells:
            if (cell.row, cell.col) == (pos[0], pos[1]):
                return cell
            
        # checking rows, cols, and subgroups for adding guesses on each cell
    def _not_in_row(self, row, num):
        for cell in self.table_cells:
            if cell.row == row:
                if cell.value == num:
                    return False
        return True
    
    def _not_in_col(self, col, num):
        for cell in self.table_cells:
            if cell.col == col:
                if cell.value == num:
                    return False
        return True

    def _not_in_subgroup(self, rowstart, colstart, num):
        for x in range(self.SRN):
            for y in range(self.SRN):
                current_cell = self._get_cell_from_pos((rowstart + x, colstart + y))
                if current_cell.value == num:
                    return False
        return True

    # remove numbers in guess if number already guessed in the same row, col, subgroup correctly
    def _remove_guessed_num(self, row, col, rowstart, colstart, num):
        for cell in self.table_cells:
            if cell.row == row and cell.guesses != None:
                for x_idx,guess_row_val in enumerate(cell.guesses):
                    if guess_row_val == num:
                        cell.guesses[x_idx] = 0
            if cell.col == col and cell.guesses != None:
                for y_idx,guess_col_val in enumerate(cell.guesses):
                    if guess_col_val == num:
                        cell.guesses[y_idx] = 0
        for x in range(self.SRN):
            for y in range(self.SRN):
                current_cell = self._get_cell_from_pos((rowstart + x, colstart + y))
                if current_cell.guesses != None:
                    for idx,guess_val in enumerate(current_cell.guesses):
                        if guess_val == num:
                            current_cell.guesses[idx] = 0

    def handle_mouse_click(self, pos):
        x, y = pos[0], pos[1]
    
    # getting table cell clicked
        if x <= width and y <= height:
            x = x // cell_size[0]
            y = y // cell_size[1]
            clicked_cell = self._get_cell_from_pos((x, y))
            self.clicked_cell = clicked_cell
            print(f"Cell selected at ({self.clicked_cell.row}, {self.clicked_cell.col})") # Debugging: Confirm cell selection
        
        # if clicked empty cell
            if self.clicked_cell and self.clicked_cell.value == 0:
                self.making_move = True
        
        # clicked unempty cell but with wrong number guess
            elif clicked_cell.value != 0 and clicked_cell.value != self.answers[y][x]:
                self.cell_to_empty = clicked_cell
        
    # deleting numbers
        elif x <= (cell_size[0] * 3) and y >= (height + cell_size[1]) and y <= (height + cell_size[1] * 2):
            if self.cell_to_empty:
                self.cell_to_empty.value = 0
                self.cell_to_empty = None
    
    # selecting modes
        elif x >= (cell_size[0] * 6) and y >= (height + cell_size[1]) and y <= (height + cell_size[1] * 2):
            self.guess_mode = True if not self.guess_mode else False
    
    # if making a move
        if self.clicked_num_below and self.clicked_cell != None and self.clicked_cell.value == 0:
            current_row = self.clicked_cell.row
            current_col = self.clicked_cell.col
            rowstart = self.clicked_cell.row - self.clicked_cell.row % self.SRN
            colstart = self.clicked_cell.col - self.clicked_cell.col % self.SRN
            if self.guess_mode:
    
    # checking the vertical group, the horizontal group, and the subgroup
                if self.clicked_num_below != self.answers[self.clicked_cell.col][self.clicked_cell.row]:
                # If in "Guess On" mode and the guess is wrong, subtract one from Lives left
                    self.lives -= 1
                if self._not_in_row(current_row, self.clicked_num_below) and self._not_in_col(current_col, self.clicked_num_below):
                    if self._not_in_subgroup(rowstart, colstart, self.clicked_num_below):
                        if self.clicked_cell.guesses != None:
                            self.clicked_cell.guesses[self.clicked_num_below - 1] = self.clicked_num_below
            else:
                self.clicked_cell.value = self.clicked_num_below
    
    # if the player guess correctly
                if self.clicked_num_below == self.answers[self.clicked_cell.col][self.clicked_cell.row]:
                    self.clicked_cell.is_correct_guess = True
                    self.clicked_cell.guesses = None
                    self._remove_guessed_num(current_row, current_col, rowstart, colstart, self.clicked_num_below)
    
    # if guess is wrong
                else:
                    self.clicked_cell.is_correct_guess = False
                    self.clicked_cell.guesses = [0 for x in range(9)]
                    self.lives -= 1
            self.clicked_num_below = None
            self.making_move = False
        else:
            self.clicked_num_below = None


    def handle_keyboard_input(self, key):
        print(f"Key pressed: {key}") # Debugging: Print the key code
        if key == pygame.K_DELETE:
            print("Delete key detected")
            # Logic to handle the "Delete" key press
            if self.clicked_cell:
                print(f"Clearing cell at ({self.clicked_cell.row}, {self.clicked_cell.col})") # Debugging print statement
                self.clicked_cell.value = 0
                 # Optionally, reset any other state related to the cell, such as guesses or correctness flags
                self.clicked_cell.is_correct_guess = None
                print(f"Cell at ({self.clicked_cell.row}, {self.clicked_cell.col}) cleared") # Debugging print statement
            else:
                print("Key is not Delete")
                
        if self.clicked_cell and self.clicked_cell.value == 0:
            num = key - pygame.K_0 # Convert the key to a number (1-9)
            if num >= 1 and num <= 9:
                self.clicked_cell.value = num
            if self.clicked_cell.value == self.answers[self.clicked_cell.col][self.clicked_cell.row]:
                self.clicked_cell.is_correct_guess = True
                
                # Additional logic to handle a correct guess
            else:
                self.clicked_cell.is_correct_guess = False
                print(f"Before decrement: {self.lives}") # Debugging line
                self.lives -= 1 # Decrement lives count for an incorrect guess
                print(f"After decrement: {self.lives}") # Debugging line
                # Handle an incorrect guess

    def _puzzle_solved(self):
        check = None
        for cell in self.table_cells:
            if cell.value == self.answers[cell.col][cell.row]:
                check = True
            else:
                check = False
                break
        return check
    
    def update(self):
        [cell.update(self.screen, self.SRN) for cell in self.table_cells]
        # [num.update(self.screen) for num in self.num_choices]
        self._draw_grid()
        self._draw_buttons()
        if self._puzzle_solved() or self.lives == 0:
            self.clock.stop_timer()
            self.game_over = True
        else:
            self.clock.update_timer()
        
        self.screen.blit(self.clock.display_timer(), (width // self.SRN,height + cell_size[1]))

    
