import random

class Sudoku:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]  # Inicializa o tabuleiro vazio
        self.generate_initial_board()

    def generate_initial_board(self):
        self.solve_sudoku()
        for _ in range(40):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0

    def solve_sudoku(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:  # Se não há mais células vazias, o Sudoku está resolvido
            return True

        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0  # Reverte a tentativa

        return False  # Nenhuma solução encontrada

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def set_cell(self, row, col, value):
        self.board[row][col] = value

    def get_cell(self, row, col):
        return self.board[row][col]

    def is_valid_move(self, row, col, value):
        for i in range(9):
            if self.board[row][i] == value or self.board[i][col] == value:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == value:
                    return False

        return True
    
    def is_solved(self):
        # Verifica se todas as células estão preenchidas
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False

        # Verifica se todas as linhas, colunas e blocos estão preenchidos corretamente
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                self.board[i][j] = 0
                if not self.is_valid_move(i, j, num):
                    self.board[i][j] = num
                    return False
                self.board[i][j] = num

        return True
