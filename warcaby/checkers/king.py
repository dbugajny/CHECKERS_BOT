from .constants import *
from .piece import Piece


class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def draw(self, win):
        if self.color == WHITE:
            win.blit(white_king_img, (self.x - SQUARE_SIZE // 2, self.y - SQUARE_SIZE // 2))
        else:
            win.blit(black_king_img, (self.x - SQUARE_SIZE // 2, self.y - SQUARE_SIZE // 2))

    def repr(self):
        return -1 if self.color == BLACK else 1

    def get_valid_moves(self, board, killer=False):
        # check if there is possibility to kill (all 4 directions)
        found_possibility_to_kill = []

        # jump: right bottom
        for i in range(1, ROWS - 1):
            if self.row + i <= ROWS - 2 and self.col + i <= ROWS - 2:
                if board[self.row + i][self.col + i]:
                    if board[self.row + i][self.col + i].color == self.color:
                        break
                    if board[self.row + i + 1][self.col + i + 1] and board[self.row + i + 1][self.col + i + 1].color != self.color:
                        break
                found_possibility_to_kill.append(self.check_jump(board, i, i, True))
                if found_possibility_to_kill[-1]:
                    break

        # jump: left bottom
        for i in range(1, ROWS - 1):
            if self.row + i <= ROWS - 2 and self.col - i >= 1:
                if board[self.row + i][self.col - i]:
                    if board[self.row + i][self.col - i].color == self.color:
                        break
                    if board[self.row + i + 1][self.col - i - 1] and board[self.row + i + 1][self.col - i - 1].color != self.color:
                        break
                found_possibility_to_kill.append(self.check_jump(board, i, -i, True))
                if found_possibility_to_kill[-1]:
                    break

        # jump: right upper
        for i in range(1, ROWS - 1):
            if self.row - i >= 1 and self.col + i <= ROWS - 2:
                if board[self.row - i][self.col + i]:
                    if board[self.row - i][self.col + i].color == self.color:
                        break
                    if board[self.row - i - 1][self.col + i + 1] and board[self.row - i - 1][self.col + i + 1].color != self.color:
                        break
                found_possibility_to_kill.append(self.check_jump(board, -i, i, True))
                if found_possibility_to_kill[-1]:
                    break

        # jump: left upper
        for i in range(1, ROWS - 1):
            if self.row - i >= 1 and self.col - i >= 1:
                if board[self.row - i][self.col - i]:
                    if board[self.row - i][self.col - i].color == self.color:
                        break
                    if board[self.row - i - 1][self.col - i - 1] and board[self.row - i - 1][self.col - i - 1].color != self.color:
                        break
                found_possibility_to_kill.append(self.check_jump(board, -i, -i, True))
                if found_possibility_to_kill[-1]:
                    break

        if killer or True in found_possibility_to_kill:
            return

        for i in range(1, ROWS - 1):
            if self.row + i <= ROWS - 1 and self.col + i <= ROWS - 1:
                if board[self.row + i][self.col + i]:
                    break
                if not (self.row + i, self.col + i) in self.valid_moves:
                    self.valid_moves.append((self.row + i, self.col + i))

        for i in range(1, ROWS - 1):
            if self.row + i <= ROWS - 1 and self.col - i >= 0:
                if board[self.row + i][self.col - i]:
                    break
                if not (self.row + i, self.col - i) in self.valid_moves:
                    self.valid_moves.append((self.row + i, self.col - i))

        for i in range(1, ROWS - 1):
            if self.row - i >= 0 and self.col + i <= ROWS - 1:
                if board[self.row - i][self.col + i]:
                    break
                if not (self.row - i, self.col + i) in self.valid_moves:
                    self.valid_moves.append((self.row - i, self.col + i))

        for i in range(1, ROWS - 1):
            if self.row - i >= 0 and self.col - i >= 0:
                if board[self.row - i][self.col - i]:
                    break
                if not (self.row - i, self.col - i) in self.valid_moves:
                    self.valid_moves.append((self.row - i, self.col - i))