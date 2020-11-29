import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np


class WebHandling:
    TIME_TO_WAIT = 2
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    URL = "https://www.chess.com/play/computer"
    BOARD_XPATH = "//*[@id=\"board-vs-personalities\"]"

    def __init__(self):
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.maximize_window()
        self.driver.get(self.URL)
        self._start_game()

    def _start_game(self, time_to_wait=2):
        time.sleep(time_to_wait)
        try:
            self.driver.implicitly_wait(time_to_wait)
            close_cookies = self.driver.find_element_by_xpath("//*[@id=\"cookie-banner\"]/div/button/span")
            close_cookies.click()
        finally:
            pass

        self.driver.implicitly_wait(time_to_wait)
        opponent = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/section/div/div/div[2]/div[2]/div[1]")
        opponent.click()

        self.driver.implicitly_wait(time_to_wait)
        choose_button = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]")
        choose_button.click()

        self.driver.implicitly_wait(time_to_wait)
        help_button = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/section/div/div[2]/div[1]/div")
        help_button.click()

        self.driver.implicitly_wait(time_to_wait)
        color_button = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/section/div/div[1]/div[1]")
        # last div number - 1 white, 2 - random, 3 - black
        color_button.click()

        self.driver.implicitly_wait(time_to_wait)
        play_button = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]")
        play_button.click()

    def get_valid_moves(self, piece: (int, int), color):
        self.click_board(piece)
        # self.driver.implicitly_wait(1)
        html_string = self.driver.find_element_by_xpath(self.BOARD_XPATH).get_attribute('innerHTML')
        pattern = r'<div data-test-element="hint" class="hint square-([\d]{2})'
        valid_moves_string = re.findall(pattern, html_string)
        valid_moves = []
        for move in valid_moves_string:
            if color == 'w':
                row, col = int(move[0]) - 1, 7 - (int(move[1]) - 1)
            else:
                row, col = 7 - (int(move[0]) - 1), int(move[1]) - 1
            valid_moves.append((col, row))
        return valid_moves

    def get_board(self, color):
        html_string = self.driver.find_element_by_xpath(self.BOARD_XPATH).get_attribute('innerHTML')
        pattern = r'<div class="piece ([a-z]{2}) square-([\d]{2})'
        pieces = re.findall(pattern, html_string)
        board = [[0 for _ in range(8)] for _ in range(8)]
        for piece in pieces:
            piece_type = piece[0]
            row, col = piece[1][0], piece[1][1]
            row, col = int(row) - 1, int(col) - 1
            board[row][col] = piece_type
        return np.rot90(np.array(board)) if color == 'w' else np.rot90(np.array(board), 3)

    def get_sizes(self):
        board = self.driver.find_element_by_xpath(self.BOARD_XPATH)
        return board.size['height'], board.size['height'] // 8

    def click_board(self, position: (int, int)):  # row and col start indexing from 0
        row, col = position[0], position[1]
        square_size = self.get_sizes()[1]
        action = ActionChains(self.driver)
        board_position = self.driver.find_element_by_xpath(self.BOARD_XPATH)
        action.move_to_element_with_offset(board_position, square_size * (col + 0.5), square_size * (row + 0.5))
        action.click()
        action.perform()

    def get_turn(self) -> str:
        html_string = self.driver.find_element_by_xpath("/html/body/div[4]/vertical-move-list").get_attribute('innerHTML')
        pattern = r'<div data-ply="[\d]+" class="(black|white) node selected">'
        last_move = re.search(pattern, html_string)
        if last_move and last_move.group(1) == 'white':
            return 'b'
        else:
            return 'w'

    def get_bot_color(self):
        html_string = self.driver.find_element_by_xpath("/html/body/div[2]").get_attribute('innerHTML')
        pattern = r'layout-board board flipped'
        if re.search(pattern, html_string):
            return 'b'
        else:
            return 'w'
