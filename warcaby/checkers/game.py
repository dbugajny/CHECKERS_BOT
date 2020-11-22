import pygame
from .board import Board
from .constants import *
from .pieces import Pawn
from copy import deepcopy


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def _init(self):
        self.selected = None
        self.selected2 = None
        self.board = Board()
        self.turn = BLACK  # black starts
        self.all_valid_moves = {}  # all valid moves for player, which turn is
        self.killer = None
        self.find_all_valid_moves()

    def winner(self):
        if self.all_valid_moves:
            return False
        elif self.turn == BLACK:
            return WHITE
        else:
            return BLACK

    def reset(self):
        self._init()

    def update(self):
        self.board.draw_board(self.win)
        if self.selected:
            self.draw_valid_moves(self.selected)
        pygame.display.update()

    def draw_valid_moves(self, piece):
        if (piece.row, piece.col) not in self.all_valid_moves:
            return
        for move in self.all_valid_moves[(piece.row, piece.col)]:
            row, col = move
            pygame.draw.circle(self.win, GREEN,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        self.selected = piece
        if self.selected:
            if self.selected.color != self.turn:
                self.selected = None
                self.selected2 = None
            self.selected2 = self.selected
        elif self.selected2 and (row, col) in self.all_valid_moves[(self.selected2.row, self.selected2.col)]:
            self.killer = self.board.move(self.selected2, row, col)
            if not self.killer:
                self.selected = None
                self.selected2 = None
                self.change_turn()
                return
            else:
                self.find_all_valid_moves()
                if not self.all_valid_moves[(self.killer[0], self.killer[1])]:
                    self.killer = None
                    self.selected = None
                    self.selected2 = None
                    self.change_turn()
                    return

    def change_turn(self):
        self.all_valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK
        self.find_all_valid_moves()

    def find_all_valid_moves(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row, col) in self.all_valid_moves:
                    del self.all_valid_moves[(row, col)]
                if self.board.board[row][col] and self.board.board[row][col].color == self.turn:
                    self.board.board[row][col].valid_moves = []
                    self.board.board[row][col].killed = {}
                    self.board.board[row][col].get_valid_moves(self.board.board, self.killer)
                    self.all_valid_moves[(row, col)] = self.board.board[row][col].valid_moves

        if self.killer:
            for row in range(ROWS):
                for col in range(COLS):
                    if self.board.board[row][col] and self.board.board[row][col].color == self.turn and (
                            row != self.killer[0] or col != self.killer[1]):
                        self.all_valid_moves[(row, col)] = []

        found_possibility_to_kill = False
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.board[row][col] and self.board.board[row][col].killed:
                    found_possibility_to_kill = True

        if not found_possibility_to_kill:
            return

        for row in range(ROWS):
            for col in range(COLS):
                if self.board.board[row][col] and self.board.board[row][col].color == self.turn and not \
                        self.board.board[row][col].killed:
                    self.all_valid_moves[(row, col)] = []
