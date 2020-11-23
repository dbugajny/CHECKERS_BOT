from .constants import *
from copy import deepcopy


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.valid_moves = []
        self.killed = {}  # dic (which move) : [which is killed]

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def check_jump(self, board, param1, param2):
        a = -1 if param1 < 0 else 1
        b = -1 if param2 < 0 else 1
        if board[self.row + param1][self.col + param2] and board[self.row + param1][
            self.col + param2].color != self.color and not board[self.row + param1 + a][self.col + param2 + b]:
            if (self.row + param1 + a, self.col + param2 + b) not in self.valid_moves:
                self.valid_moves.append((self.row + param1 + a, self.col + param2 + b))
                self.killed[(self.row + param1 + a, self.col + param2 + b)] = (self.row + param1, self.col + param2)
            return True
        return False

    def __repr__(self):
        return "BLACK" if self.color == BLACK else "WHITE"


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
        for i in range(ROWS - 1):
            if self.row + i <= ROWS - 3 and self.col + i <= ROWS - 3:
                if board[self.row + i][self.col + i] and board[self.row + i][self.col + i].color != self.color:
                    if board[self.row + i + 1][self.col + i + 1] and board[self.row + i][self.col + i].color != self.color:
                        break
                found_possibility_to_kill.append(self.check_jump(board, i, i))
                if found_possibility_to_kill[-1]:
                    break

        # jump: left bottom
        for i in range(ROWS - 1):
            if self.row + i <= ROWS - 3 and self.col - i >= 2:
                if board[self.row + i][self.col - i] and board[self.row + i][self.col - i].color != self.color:
                    if board[self.row + i + 1][self.col - i - 1] and board[self.row + i + 1][self.col - i - 1].color != self.color:
                        break
                found_possibility_to_kill.append(self.check_jump(board, i, -i))
                if found_possibility_to_kill[-1]:
                    break

        # jump: right upper
        for i in range(ROWS - 1):
            if self.row - i >= 2 and self.col + i <= ROWS - 3:
                if board[self.row - i][self.col + i] and board[self.row - i][self.col + i].color != self.color:
                    if board[self.row - i - 1][self.col + i + 1] and board[self.row - i - 1][self.col + i + 1].color != self.color:
                        break
                found_possibility_to_kill.append(self.check_jump(board, -i, i))
                if found_possibility_to_kill[-1]:
                    break

        # jump: left upper
        for i in range(ROWS - 1):
            if self.row - i >= 2 and self.col - i >= 2:
                if board[self.row - i][self.col - i] and board[self.row - i][self.col - i].color != self.color:
                    if board[self.row - i - 1][self.col - i - 1] and board[self.row - i - 1][self.col - i - 1].color != self.color:
                        break
                found_possibility_to_kill.append(self.check_jump(board, -i, -i))
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
