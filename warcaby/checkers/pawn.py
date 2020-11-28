from .constants import *
from .piece import Piece

class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def draw(self, win):
        if self.color == WHITE:
            win.blit(white_pawn_img, (self.x - SQUARE_SIZE // 2, self.y - SQUARE_SIZE // 2))
        else:
            win.blit(black_pawn_img, (self.x - SQUARE_SIZE // 2, self.y - SQUARE_SIZE // 2))

    def repr(self):
        return -1 if self.color == BLACK else 1

    def get_valid_moves(self, board, killer=False):

        # check if there is possibility to kill (all 4 directions)
        found_possibility_to_kill = []
        # jump: right bottom
        if self.row <= ROWS - 3 and self.col <= ROWS - 3:
            found_possibility_to_kill.append(self.check_jump(board, 1, 1))
        # jump: left bottom
        if self.row <= ROWS - 3 and self.col >= 2:
            found_possibility_to_kill.append(self.check_jump(board, 1, -1))
        # jump: right upper
        if self.row >= 2 and self.col <= ROWS - 3:
            found_possibility_to_kill.append(self.check_jump(board, -1, 1))
        # jump: left upper
        if self.row >= 2 and self.col >= 2:
            found_possibility_to_kill.append(self.check_jump(board, -1, -1))

        if killer or True in found_possibility_to_kill:
            return

        if self.color == BLACK:
            if self.col > 0 and not board[self.row - 1][self.col - 1]:
                if (self.row - 1, self.col - 1) not in self.valid_moves:
                    self.valid_moves.append((self.row - 1, self.col - 1))
            if self.col <= ROWS - 2 and not board[self.row - 1][self.col + 1]:
                if (self.row - 1, self.col + 1) not in self.valid_moves:
                    self.valid_moves.append((self.row - 1, self.col + 1))

        if self.color == WHITE:
            if self.col > 0 and not board[self.row + 1][self.col - 1]:
                if (self.row + 1, self.col - 1) not in self.valid_moves:
                    self.valid_moves.append((self.row + 1, self.col - 1))
            if self.col <= ROWS - 2 and not board[self.row + 1][self.col + 1]:
                if (self.row + 1, self.col + 1) not in self.valid_moves:
                    self.valid_moves.append((self.row + 1, self.col + 1))
