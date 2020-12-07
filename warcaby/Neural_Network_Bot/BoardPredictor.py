import pygame
from warcaby.checkers.board import Board
from warcaby.checkers import pawn, king
from warcaby.checkers.constants import *


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

class BoardPredictor:
    def __init__(self, win):
        self.board = Board()
        self.win = win

    def make_piece(self, row, col, key):
        # q w e r t
        if key == 113:
            self.board.board[row][col] = pawn.Pawn(row, col, WHITE)
        elif key == 119:
            self.board.board[row][col] = pawn.Pawn(row, col, BLACK)
        elif key == 101:
            self.board.board[row][col] = king.King(row, col, WHITE)
        elif key == 114:
            self.board.board[row][col] = king.King(row, col, BLACK)
        elif key == 116:
            self.board.board[row][col] = 0

    def update(self):
        self.board.draw_board(self.win)
        pygame.display.update()

    def get_board_rate(self):
        import random
        return random.uniform(0, 1)

    def clean_board(self):
        for row in range(ROWS):
            for col in range(ROWS):
                self.board.board[row][col] = 0

def board_predict():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('BOARD PREDICT')
    board_predictor = BoardPredictor(WIN)
    run = True
    row, col = None, None
    print("OZNACZENIE KLAWISZY")
    print("q - bialy pionek")
    print("w - czarny pionek")
    print("e - biala damka")
    print("r - czarna damka")
    print("t - usuniecie")
    print("u - rate")
    print("o - reset szchowiny")
    print("p - usuniecie calej szachowiny")
    print("esc - wyjscie")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    run = False
                elif event.key in [113, 119, 101, 114, 116] and row is not None and col is not None:
                    board_predictor.make_piece(row, col, event.key)
                elif event.key == 111:
                    board_predictor = BoardPredictor(WIN)
                elif event.key == 112:
                    board_predictor.clean_board()
                elif event.key == 117:
                    rate = board_predictor.get_board_rate()
                    print(f"ACTUAL RATE: {rate:.3f}")

        board_predictor.update()
