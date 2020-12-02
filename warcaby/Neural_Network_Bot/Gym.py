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
        self.epochs = 0
        self.white_history = []
        self.black_history = []

    def self_play(self):
        run = True
        while run:
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         sys.exit()

            if self.game.winner():
                run = False
                if self.game.winner() == Color.WHITE:
                    self.white_wins += 1
                    self.white_player.game_result = 1
                    self.black_player.game_result = 0
                    self.white_history.append(1)
                    self.black_history.append(0)
                if self.game.winner() == Color.BLACK:
                    self.black_wins += 1
                    self.white_player.game_result = 0
                    self.black_player.game_result = 1
                    self.white_history.append(0)
                    self.black_history.append(1)
                break

            move_param = self.game.get_all_possible_board_states_and_moves()

            if self.game.turn == BLACK:
                move = self.black_player.pick_move(move_param[0], move_param[1])
                self.game.select_by_giving(move[0].row, move[0].col, move[1], move[2])
            else:
                move = self.white_player.pick_move(move_param[0], move_param[1])
                self.game.select_by_giving(move[0].row, move[0].col, move[1], move[2])

    def play_against_bot(self):

        def get_row_col_from_mouse(pos):
            x, y = pos
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE
            return row, col

        clock = pg.time.Clock()
        run = True
        row, col = 0, 0
        FPS = 10
        while run:
            if self.game.winner():
                run = False
                break
            clock.tick(FPS)

            if self.game.turn == BLACK:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                        self.game.select(row, col)
            else:
                move_param = self.game.get_all_possible_board_states_and_moves()
                move = self.white_player.pick_move(move_param[0], move_param[1])
                self.game.select_by_giving(move[0].row, move[0].col, move[1], move[2])

            self.game.update()

    def players_learn(self):
        self.black_player.learn_from_game_data()
        self.white_player.learn_from_game_data()

    def train_models(self, epochs):
        for i in range(epochs):
            self.self_play()
            self.players_learn()
            self.game = Game(self.window)
            print("czarne: ", self.black_wins, " białe: ", self.white_wins)
            if i % 50 == 0:
                self.save_models()
            self.epochs += 1

    def save_models(self):
        print("saving")
        self.white_player.brain.model.save('Neural_Network_Bot/saved_models/white.h5')
        self.black_player.brain.model.save('Neural_Network_Bot/saved_models/black.h5')
