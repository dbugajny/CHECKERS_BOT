from .constants import *
from copy import deepcopy
from abc import abstractmethod, ABC


class Piece(ABC):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.valid_moves = []
        self.killed = {}  # dic (which move) : [which is killed]
        self.max_moves = 0

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def check_jump(self, board, param1, param2, king=False):
        a = -1 if param1 < 0 else 1
        b = -1 if param2 < 0 else 1
        if board[self.row + param1][self.col + param2] and board[self.row + param1][
            self.col + param2].color != self.color and not board[self.row + param1 + a][self.col + param2 + b]:
            if (self.row + param1 + a, self.col + param2 + b) not in self.valid_moves:
                self.valid_moves.append((self.row + param1 + a, self.col + param2 + b))
                self.killed[(self.row + param1 + a, self.col + param2 + b)] = (self.row + param1, self.col + param2)

            if king:
                for i in range(1, ROWS - 1):
                    if 0 <= self.row + i * a + param1 <= ROWS - 1 and 0 <= self.col + i * b + param2 <= ROWS - 1:

                        if not board[self.row + i * a + param1][self.col + i * b + param2]:
                            if (self.row + i * a + param1, self.col + i * b + param2) not in self.valid_moves:
                                self.valid_moves.append((self.row + i * a + param1, self.col + i * b + param2))
                                self.killed[(self.row + i * a + param1, self.col + i * b + param2)] = (
                                    self.row + param1, self.col + param2)
                        else:
                            return True
            return True
        return False

    @abstractmethod
    def get_valid_moves(self, board, killer=False):
        pass

    def __repr__(self):
        return "BLACK" if self.color == BLACK else "WHITE"
