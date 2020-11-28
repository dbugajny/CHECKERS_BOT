import os
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow import keras
from keras import layers


class Board_Evaluator():
    def __init__(self, layers_specification):  # layers_specification is array of tuples describing network
        self.model = keras.Sequential()
        self.model.add(keras.Input(shape=64))  # board has 64 squares

        for layer in layers_specification:
            self.model.add(layers.Dense(units=layer[0], activation=layer[1]))

        self.model.add(layers.Dense(1, activation="sigmoid"))  # single output for rating
        self.model.compile(
            loss=keras.losses.BinaryCrossentropy(from_logits=True),
            optimizer=keras.optimizers.Adam(lr=0.01),
            metrics=["accuracy"])

    def rate_board_state(self, board):
        input_data = np.asarray(board).astype('float32').reshape(64)
        answer = self.model.predict(np.array([input_data]))
        return answer[0][0]

    def learn_from_played_game(self, game_data, game_label):
        batch_size = len(game_data)
        x_train = np.asarray(game_data).reshape(len(game_data), 64)
        y_train = np.full((len(game_data)), game_label)
        self.model.fit(x_train, y_train, batch_size=batch_size, epochs=1, verbose=0)
