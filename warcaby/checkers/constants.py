from enum import Enum
import pygame


class Color(Enum):
    WHITE = 0
    BLACK = 1


BLACK = Color.BLACK
WHITE = Color.WHITE


WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

GREEN = (25, 75, 25)

white_pawn_img = pygame.image.load('images/white_pawn_img.png')
black_pawn_img = pygame.image.load('images/black_pawn_img.png')
white_king_img = pygame.image.load('images/white_king_img.png')
black_king_img = pygame.image.load('images/black_king_img.png')
board_img = pygame.image.load('images/board_img.png')
