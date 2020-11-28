import pygame as pg
import sys
from warcaby.checkers.constants import *
from warcaby.checkers.game import *
from warcaby.checkers.board import get_table
from warcaby.Neural_Network_Bot.Player import Player


class Gym:
    def __init__(self, black_player, white_player, WIN):
        self.game = Game(WIN)
        self.black_player = black_player
        self.white_player = white_player
        self.window = WIN
        self.black_wins = 0
        self.white_wins = 0

    def play_game(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.game.winner():
                run = False
                self.white_player.game_result, self.black_player.game_result = self.game.labels[0], self.game.labels[1]
                if self.game.winner() == Color.WHITE:
                    self.white_wins += 1
                if self.game.winner() == Color.BLACK:
                    self.black_wins += 1
                break

            self.game.board.draw_board(self.window)
            pg.time.delay(250)
            move_param = self.game.get_all_possible_board_states_and_moves()

            if self.game.turn == BLACK:
                move = self.black_player.pick_move(move_param[0], move_param[1])
                self.game.select_by_giving(move[0].row, move[0].col, move[1], move[2])
            else:
                move = self.white_player.pick_move(move_param[0], move_param[1])
                self.game.select_by_giving(move[0].row, move[0].col, move[1], move[2])

            self.game.board.draw_board(self.window)
            pg.time.delay(250)

    def players_learn(self):
        self.black_player.learn_from_game_data()
        self.white_player.learn_from_game_data()

    def train_models(self, epochs):
        for i in range(epochs):
            self.play_game()
            self.players_learn()
            self.game = Game(self.window)
