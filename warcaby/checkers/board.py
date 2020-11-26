from .constants import *
from .pieces import *
from copy import deepcopy


def get_table(tab):  # return representation of table as MATRIX (-2, -1, 0 , 1, 2 - pieces)
    table = deepcopy(tab)
    for row in range(ROWS):
        for col in range(COLS):
            if tab[row][col]:
                table[row][col] = tab[row][col].repr()
    return table


def move_result(tab, piece_row, piece_col, row, col):  # give result what will happen when we choose given move
    table = deepcopy(tab)
    piece = table[piece_row][piece_col]
    table[row][col], table[piece.row][piece.col] = table[piece.row][piece.col], table[row][col]
    if row == ROWS - 1 and piece.color == WHITE or row == 0 and piece.color == BLACK:
        table[piece.row][piece.col] = King(piece.row, piece.col, piece.color) # making king
    if (row, col) in piece.killed:
        table[row][col] = 0
    return get_table(table)



class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):  # change piece to new position (row, col)
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], self.board[row][col]
        piece.move_piece(row, col)
        if row == ROWS - 1 and piece.color == WHITE or row == 0 and piece.color == BLACK:
            self.board[piece.row][piece.col] = King(piece.row, piece.col, piece.color) # making king
        if (row, col) in piece.killed:
            r, c = piece.killed[(row, col)]
            self.remove(r, c)
            return piece.row, piece.col

    def remove(self, row, col):
        self.board[row][col] = 0

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Pawn(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Pawn(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_board(self, win):
        win.blit(board_img, (0, 0))
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
