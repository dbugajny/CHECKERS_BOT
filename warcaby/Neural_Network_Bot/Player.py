from Board_evaluator import Board_Evaluator
from math import random


def get_index_by_elements_probability(array):
    new_array = [0]
    for num in array:
        new_array.append(num + new_array[-1])
    sum_of_array = sum(new_array)
    pick = random.unform(0.0000001, sum_of_array - 0.0000001)  # for safety
    index = 0
    while pick < new_array[index]:  # could change to binary search to improve efficiency
        index += 1
    return index - 1


class Player:
    def __init__(self, color, brain_properties):
        self.color = color
        self.brain = Board_Evaluator(brain_properties)
        self.game_experience = []
        self.game_result = None

    def pick_move_from_possible_move_states(self, array_of_possible_boards):
        rates_of_board = []
        for board in array_of_possible_boards:
            rates_of_board.append(self.brain.rate_board_state(board))

        #picked_index = get_index_by_elements_probability(rates_of_board)
        picked_board = random.choices(array_of_possible_boards, rates_of_board)
        self.add_data_from_chosen_move(picked_board)
        return picked_board

    def add_data_from_chosen_move(self, chosen_board):
        self.game_experience.append(chosen_board)

    def reset(self):
        self.game_experience = []
        self.game_result = None

    def learn_from_game_data(self):
        self.brain.learn_from_played_game(self.game_experience, self.game_result)
        self.reset()
