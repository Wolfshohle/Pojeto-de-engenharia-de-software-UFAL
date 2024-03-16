import pygame
import sys
import pygame_gui
import os

# Definição das cores
WHITE = (255, 255, 255)
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Menu Principal")
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Carrega a imagem Sudoku
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(script_dir, 'Assets')
        sudoku_image_path = os.path.join(assets_dir, 'Titulo.png')
        if os.path.exists(sudoku_image_path):
            sudoku_image = pygame.image.load(sudoku_image_path).convert_alpha()
        else:
            raise FileNotFoundError(f"Arquivo '{sudoku_image_path}' não encontrado.")
        image_rect = sudoku_image.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.image_view = pygame_gui.elements.UIImage(relative_rect=image_rect,
                                                      image_surface=sudoku_image,
                                                      manager=self.manager)

        # Carrega a imagem do botão Jogar
        jogar_image_path = os.path.join(assets_dir, 'Jogar.png')
        if os.path.exists(jogar_image_path):
            jogar_image = pygame.image.load(jogar_image_path).convert_alpha()
        else:
            raise FileNotFoundError(f"Arquivo '{jogar_image_path}' não encontrado.")

        # Cria um botão invisível para jogar
        jogar_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, 400), (200, 50))
        self.play_button = pygame_gui.elements.UIButton(relative_rect=jogar_rect,
                                                        text='',
                                                        manager=self.manager)

        # Sobreposição da imagem sobre o botão invisível
        self.jogar_overlay = pygame_gui.elements.UIImage(relative_rect=jogar_rect,
                                                         image_surface=jogar_image,
                                                         manager=self.manager)

        # Carrega a imagem do botão Sair
        sair_image_path = os.path.join(assets_dir, 'Sair.png')
        if os.path.exists(sair_image_path):
            sair_image = pygame.image.load(sair_image_path).convert_alpha()
        else:
            raise FileNotFoundError(f"Arquivo '{sair_image_path}' não encontrado.")

        # Obtenha o retângulo da imagem do botão Sair
        sair_image_rect = sair_image.get_rect()

        # Calcule a posição para centralizar o botão Sair
        sair_rect = pygame.Rect((SCREEN_WIDTH // 2 - sair_image_rect.width // 2, 470), sair_image_rect.size)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=sair_rect,
                                                        text='',
                                                        manager=self.manager)

        # Sobreposição da imagem sobre o botão invisível
        self.sair_overlay = pygame_gui.elements.UIImage(relative_rect=sair_rect,
                                                         image_surface=sair_image,
                                                         manager=self.manager)

        self.next_screen = None

    def run(self):
        running = True

        while running:
            time_delta = self.clock.tick(30) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.play_button or event.ui_element == self.jogar_overlay:
                            self.next_screen = 'play'
                            running = False
                        elif event.ui_element == self.quit_button or event.ui_element == self.sair_overlay:
                            self.next_screen = 'quit'
                            running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.screen.fill(WHITE)  # Preenche com branco para o fundo
            self.manager.draw_ui(self.screen)
            pygame.display.update()

        return self.next_screen

