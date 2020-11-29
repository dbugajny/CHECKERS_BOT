from web_driver import WebHandling
from copy import deepcopy
import random
import time


class Game:
    def __init__(self):
        self.web_handler = WebHandling()
        self.bot_color = self.web_handler.get_bot_color()
        self.board = self.web_handler.get_board(self.bot_color)
        self.turn = self.web_handler.get_turn()
        self.valid_moves = {}

    def find_all_valid_moves(self):
        self.turn = self.web_handler.get_turn()
        while self.bot_color != self.turn:
            self.turn = self.web_handler.get_turn()
        self.valid_moves = {}
        self.board = self.web_handler.get_board(self.bot_color)
        for row in range(8):
            for col in range(8):
                if self.board[row][col] and self.board[row][col][0] == self.turn:
                    self.valid_moves[(row, col)] = self.web_handler.get_valid_moves((row, col), self.bot_color)

    def make_move(self):
        self.find_all_valid_moves()
        best_piece, best_move = self._get_best_move()
        self.web_handler.click_board(best_piece)
        time.sleep(1)
        self.web_handler.click_board(best_move)

    def _move_result(self, piece, move):
        move_row, move_col = move[0], move[1]
        piece_row, piece_col = piece[0], piece[1]
        board = deepcopy(self.board)
        board[piece_row][piece_col], board[move_row][move_col] = 0, board[piece_row][piece_col]
        return board

    def _get_best_move(self):
        max_evaluator = 0
        best_piece, best_move = None, None
        for piece in self.valid_moves:
            for move in self.valid_moves[piece]:
                evaluation = self._get_evaluation(piece, move)
                if evaluation >= max_evaluator:
                    max_evaluator = evaluation
                    best_piece, best_move = piece, move
        return best_piece, best_move

    def _get_evaluation(self, piece, move):
        return random.uniform(0, 1)
