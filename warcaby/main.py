import pygame
from checkers.constants import *
from checkers.game import *
from checkers.board import get_table
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
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


main_gui(WIN)