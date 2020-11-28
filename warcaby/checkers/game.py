from .board import Board, get_table, move_result
from .constants import *


class Game:
    def __init__(self, win):
        self.turns_counter = 0
        self.max_turns = 200
        self.board_history = []
        self.labels = []
        self.selected = None
        self.selected2 = None
        self.killer = None
        self.board = Board()
        self.turn = BLACK  # black starts
        self.all_valid_moves = {}  # all valid moves for player, which turn is
        self.find_all_valid_moves()
        self.win = win

    def winner(self):
        if self.turns_counter > self.max_turns:
            self.labels = [0 for _ in range(self.turns_counter)]
            return "DRAW"
        if self.all_valid_moves:
            return False
        elif self.turn == BLACK:  # maybe it should be changed with labels for WHITE
            self.labels = [1 * (-1) ** i for i in range(self.turns_counter)]
            return WHITE
        elif self.turn == WHITE:
            self.labels = [-(1 * (-1) ** i) for i in range(self.turns_counter)]
            return BLACK

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
            if not self.killer or self.selected2.row == 0 or self.selected2.row == 7:
                print(self.killer)
                print(self.selected2.row,  self.selected2.col)
                print("---------")
                self.killer = None
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

    def select_by_giving(self, row_piece, col_piece, row_destination, col_destination):
        piece = self.board.get_piece(row_piece, col_piece)
        self.killer = self.board.move(piece, row_destination, col_destination)
        if not self.killer:
            self.change_turn()
            return
        else:
            self.find_all_valid_moves()
            if not self.all_valid_moves[(self.killer[0], self.killer[1])]:
                self.killer = None
                self.change_turn()
                return

    def change_turn(self):
        self.board_history.append(get_table(self.board.board))
        self.turns_counter += 1
        self.all_valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK
        self.find_all_valid_moves()

    def find_all_valid_moves(self):
        found_possibility_to_kill = False

        for row in range(ROWS):
            for col in range(COLS):
                if (row, col) in self.all_valid_moves:
                    del self.all_valid_moves[(row, col)]
                if self.board.board[row][col] and self.board.board[row][col].color == self.turn:
                    self.board.board[row][col].valid_moves = []
                    self.board.board[row][col].killed = {}
                    self.board.board[row][col].get_valid_moves(self.board.board, self.killer)

                    if self.board.board[row][col] and self.board.board[row][col].killed:
                        found_possibility_to_kill = True

                    if not self.killer or (row == self.killer[0] or col == self.killer[1]):
                        self.all_valid_moves[(row, col)] = self.board.board[row][col].valid_moves

        if not found_possibility_to_kill:
            return

        for row in range(ROWS):
            for col in range(COLS):
                if self.board.board[row][col] and self.board.board[row][col].color == self.turn and not \
                        self.board.board[row][col].killed:
                    self.all_valid_moves[(row, col)] = []



    def get_all_possible_board_states_and_moves(self):
        board_states = []
        required_moves = []
        for piece in self.all_valid_moves:
            if len(self.all_valid_moves[piece]) > 0:
                for piece_destination in self.all_valid_moves[piece]:
                    board_states.append(
                        move_result(self.board.board, piece[0], piece[1], piece_destination[0], piece_destination[1]))
                    required_moves.append((self.board.board[piece[0]][piece[1]], piece_destination[0], piece_destination[1]))
        return board_states, required_moves
