from abc import ABC

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.optimizers import Adam
import numpy as np


class DuelingDQN(keras.models.Model, ABC):
    def __init__(self):
        super(DuelingDQN, self).__init__()

        self.dense1 = keras.layers.Dense(100, activation=keras.activations.relu)
        self.dense2 = keras.layers.Dense(50, activation=keras.activations.relu)

        self.denseV = keras.layers.Dense(10, activation=keras.activations.relu)
        self.V = keras.layers.Dense(1, activation=keras.activations.linear)

        self.denseA = keras.layers.Dense(10, activation=keras.activations.relu)
        self.A = keras.layers.Dense(1, activation=keras.activations.linear)

    def call(self, inputs, training=None, mask=None):
        inputs = list(inputs)
        if not isinstance(inputs, list):
            raise ValueError('This layer should be called on a list of inputs.')
        state = inputs[0]
        advantage_mean = inputs[1]

        x = self.dense1(state)
        x = self.dense2(x)

        Vx = self.denseV(x)
        V = self.V(Vx)

        Ax = self.denseA(x)
        A = self.A(Ax)

        Q = V + A - advantage_mean
        return Q

    def advantage(self, state):
        #print(state.shape)

        x = self.dense1(state)
        x = self.dense2(x)
        x = self.denseA(x)
        A = self.A(x)
        return A
