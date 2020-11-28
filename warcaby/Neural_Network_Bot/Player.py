from warcaby.Neural_Network_Bot.Board_evaluator import Board_Evaluator
import random

def get_index_by_elements_probability(array):
    new_array = [0]
    for num in array:
        new_array.append(num + new_array[-1])
    pick = random.uniform(0.0000001, new_array[-1] - 0.0000001)  # for safety
    index = len(new_array)-1
    while pick < new_array[index]:  # could change to binary search to improve efficiency
        index -= 1

    #print(index)
    return index


class Player:
    def __init__(self, color, brain_properties):
        self.color = color
        self.brain = Board_Evaluator(brain_properties)
        self.game_experience = []
        self.game_result = None

    def pick_index_from_possible_board_states(self, array_of_possible_boards):
        rates_of_board = []
        for board in array_of_possible_boards:
            rates_of_board.append(self.brain.rate_board_state(board))

        picked_index = get_index_by_elements_probability(rates_of_board)
        picked_board = array_of_possible_boards[picked_index]
        self.add_data_from_chosen_move(picked_board)
        return picked_index

    def add_data_from_chosen_move(self, chosen_board):
        self.game_experience.append(chosen_board)

    def reset(self):
        self.game_experience = []
        self.game_result = None

    def learn_from_game_data(self):
        self.brain.learn_from_played_game(self.game_experience, self.game_result)
        self.reset()

    def pick_move(self, array_of_possible_boards, array_required_moves):
        picked_index = self.pick_index_from_possible_board_states(array_of_possible_boards)
        return array_required_moves[picked_index]


