import pygame
from warcaby.checkers.constants import *
from warcaby.checkers.game import *
from warcaby.checkers.board import get_table
from warcaby.Neural_Network_Bot.Board_evaluator import Board_Evaluator
from warcaby.Neural_Network_Bot.Gym import Gym
from warcaby.Neural_Network_Bot.Player import Player

FPS = 60

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CHECKERS')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main_gui(window):
    run = True
    clock = pygame.time.Clock()
    game = Game(window)
    predictor = Board_Evaluator([(50, 'relu')])

    while run:
        if game.winner():
            run = False

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                game.select(row, col)

        game.update()

    pygame.quit()


def main_tui():
    print("works")
    run = True

    game = Game(None)

    while run:
        if game.winner():
            run = False

        board = get_table(game.board.board)
        for row in board:
            print(row)

        a = int(input("Give ROW (piece): "))
        b = int(input("Give COL (piece): "))
        c = int(input("Give ROW (destination): "))
        d = int(input("Give COL (destination): "))
        game.select_by_giving(a, b, c, d)  # don't check if (a, b) is valid piece and (c, d) is valid destination


def main_gym():
    black = Player("BLACK",
                   [(200, "relu")])  # second argument is path to model or array of properties
    white = Player("WHITE",
                   'Neural_Network_Bot/saved_models/white.h5')

    gym = Gym(black, white, None)
    gym.train_models(3000)


main_gym()
