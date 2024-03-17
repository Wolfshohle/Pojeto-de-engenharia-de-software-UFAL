import unittest
from Sudoku import Sudoku

class TestSudokuLogic(unittest.TestCase):
    def setUp(self):
        # Inicializa um tabuleiro de Sudoku vazio
        self.sudoku = Sudoku()

    def test_fill_cell_valid_move(self):
        # Testa o preenchimento de uma célula com um movimento válido
        self.assertTrue(self.sudoku.is_valid_move(0, 0, 1))  # Testa um movimento válido
        self.sudoku.set_cell(0, 0, 1)
        self.assertEqual(self.sudoku.get_cell(0, 0), 1)  # Verifica se a célula foi preenchida corretamente

    def test_fill_cell_invalid_move(self):
        # Testa o preenchimento de uma célula com um movimento inválido
        self.sudoku.set_cell(0, 0, 1)
        self.assertFalse(self.sudoku.is_valid_move(0, 0, 1))  # Testa um movimento inválido (mesmo número na mesma linha)
        self.assertEqual(self.sudoku.get_cell(0, 0), 1)  # Verifica se a célula não foi alterada

    def test_board_completion_valid(self):
        # Testa se um tabuleiro de Sudoku completo e válido é reconhecido como tal
        # Preenche o tabuleiro com uma solução válida
        self.sudoku.board = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        self.assertTrue(self.sudoku.is_solved())  # Verifica se o tabuleiro é reconhecido como completo e válido

    def test_board_completion_invalid(self):
        # Testa se um tabuleiro de Sudoku incompleto e válido é reconhecido como tal
        # Preenche o tabuleiro com uma solução inválida
        self.sudoku.board = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 8]  # Número repetido na última linha
        ]
        self.assertFalse(self.sudoku.is_solved())  # Verifica se o tabuleiro é reconhecido como incompleto ou inválido

if __name__ == '__main__':
    unittest.main()
