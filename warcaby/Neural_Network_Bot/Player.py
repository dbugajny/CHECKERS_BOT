from warcaby.Neural_Network_Bot.Board_evaluator import Board_Evaluator
import random


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

        picked_index = random.choices(range(len(rates_of_board)), rates_of_board)[0]
        if picked_index < 0 or picked_index > len(array_of_possible_boards) - 1:
            print(picked_index, rates_of_board)
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
