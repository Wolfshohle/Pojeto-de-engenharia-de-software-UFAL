import pygame
import sys
from Menu import Menu
from Interface import PygameSudokuInterface
from Sudoku import Sudoku

def main():
    pygame.init()
    menu = Menu()
    choice = menu.run()

    if choice == 'play':
        sudoku = Sudoku()
        sudoku_interface = PygameSudokuInterface(sudoku, return_to_menu)
        sudoku_interface.run()
    elif choice == 'quit':
        pygame.quit()
        sys.exit()

def return_to_menu():
    pygame.quit()  # Encerra a execução da interface do Sudoku
    main()  # Reinicia o menu principal

if __name__ == "__main__":
    main()
