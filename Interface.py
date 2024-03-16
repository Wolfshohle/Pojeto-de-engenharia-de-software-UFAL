import pygame
import pygame_gui
from Sudoku import Sudoku

# Definição das cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Tamanho da tela e do tabuleiro
SCREEN_WIDTH = 860  # Largura total da tela (largura do tabuleiro + largura dos botões + espaço)
SCREEN_HEIGHT = 640  # Altura da tela
CELL_SIZE = 60

class PygameSudokuInterface:
    def __init__(self, sudoku, return_to_menu_callback):
        pygame.init()
        self.sudoku = sudoku
        self.return_to_menu_callback = return_to_menu_callback
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)
        self.selected_cell = None
        self.game_over = False
        self.completed = False  # Variável de controle para rastrear se o Sudoku foi completado

        # Inicializa a interface do usuário
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Calcula a posição do Sudoku
        sudoku_position = ((SCREEN_WIDTH - 9 * CELL_SIZE - 20) // 2, (SCREEN_HEIGHT - 9 * CELL_SIZE) // 2)

        # Calcula a posição dos botões
        button_width = 140  # Largura dos botões
        button_height = 40  # Altura dos botões
        button_padding = 20  # Espaçamento entre os botões

        self.autocomplete_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((sudoku_position[0] + 9 * CELL_SIZE + button_padding, sudoku_position[1]), (button_width, button_height)),
            text='Auto completar',
            manager=self.manager
        )

        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((sudoku_position[0] + 9 * CELL_SIZE + button_padding, sudoku_position[1] + button_height + button_padding), (button_width, button_height)),
            text='Reset',
            manager=self.manager
        )

        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((sudoku_position[0] + 9 * CELL_SIZE + button_padding, sudoku_position[1] + 2 * (button_height + button_padding)), (button_width, button_height)),
            text='Voltar ao Menu',
            manager=self.manager
        )

    def draw_board(self):
        self.screen.fill(WHITE)
        
        # Desenha as grades do Sudoku
        for i in range(10):
            if i % 3 == 0:
                line_thickness = 3
            else:
                line_thickness = 1
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), (9 * CELL_SIZE, i * CELL_SIZE), line_thickness)
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, 9 * CELL_SIZE), line_thickness)

        # Desenha os números dentro das células
        for i in range(9):
            for j in range(9):
                value = self.sudoku.get_cell(i, j)
                text_color = BLACK
                if value != 0:
                    if self.selected_cell is not None and (i, j) == self.selected_cell:
                        text_color = RED if not self.sudoku.is_valid_move(i, j, value) else BLACK
                    text_surface = self.font.render(str(value), True, text_color)
                    text_rect = text_surface.get_rect(center=((j * CELL_SIZE) + CELL_SIZE // 2, (i * CELL_SIZE) + CELL_SIZE // 2))
                    self.screen.blit(text_surface, text_rect)

        # Destaca a célula selecionada
        if self.selected_cell is not None:
            pygame.draw.rect(self.screen, (0, 255, 255), pygame.Rect(self.selected_cell[1] * CELL_SIZE, self.selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

        # Desenha a mensagem "Venceu!" se o jogo estiver completo
        if self.sudoku.is_solved() and not self.completed:
            text_surface = self.font.render("Você venceu!", True, GREEN)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))  # Posição abaixo do tabuleiro
            self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True

        while running:
            time_delta = self.clock.tick(30) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    self.selected_cell = (row, col)
                elif event.type == pygame.KEYDOWN:
                    if self.selected_cell is not None:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                            value = int(pygame.key.name(event.key))
                            if self.sudoku.is_valid_move(self.selected_cell[0], self.selected_cell[1], value):
                                self.sudoku.set_cell(self.selected_cell[0], self.selected_cell[1], value)
                        elif event.key == pygame.K_BACKSPACE:
                            self.sudoku.set_cell(self.selected_cell[0], self.selected_cell[1], 0)
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element== self.autocomplete_button:
                            self.sudoku.solve_sudoku()
                        elif event.ui_element == self.reset_button:
                            self.sudoku.generate_initial_board()
                            self.completed = False  # Define a variável de controle para False
                            self.game_over = False  # Reseta a tela de vitória
                        elif event.ui_element == self.menu_button:
                            self.return_to_menu()

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.screen.fill(WHITE)
            self.draw_board()
            self.manager.draw_ui(self.screen)
            pygame.display.update()

        pygame.quit()

    def return_to_menu(self):
        self.return_to_menu_callback()
