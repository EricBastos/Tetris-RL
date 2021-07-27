from abc import ABC

import tensorflow as tf
import tensorflow.keras as keras
from noisy_net import NoisyDense

class DuelingDQN(keras.models.Model, ABC):
    def __init__(self):
        super(DuelingDQN, self).__init__()

        self.input_conv = keras.layers.Input((20, 10, 1), name='Input-Conv')
        self.input_dense = keras.layers.Input(7, name='Input-Dense')

        self.conv1 = keras.layers.Conv2D(20, (20, 1), activation='relu')(self.input_conv)
        self.conv2 = keras.layers.Conv2D(16, (1, 4), activation='relu')(self.conv1)
        self.conv3 = keras.layers.Conv2D(8, (1, 7), activation='relu')(self.conv2)

        self.flatten1 = keras.layers.Flatten()(self.conv3)
        self.conv_model = keras.Model(inputs=self.input_conv, outputs=self.flatten1, name='Conv-Model')

        self.dense1 = keras.layers.Dense(32, activation='relu')(self.input_dense)
        self.dense2 = keras.layers.Dense(16, activation='relu')(self.dense1)
        self.dense_model = keras.Model(inputs=self.input_dense, outputs=self.dense2, name='Dense-Model')

        self.concat = keras.layers.concatenate([self.conv_model.output, self.dense_model.output])
        self.concat = keras.layers.BatchNormalization()(self.concat)

        self.noiseV = NoisyDense(32)

        self.denseV = self.noiseV(self.concat)
        self.denseV = keras.layers.ReLU()(self.denseV)
        self.V = keras.layers.Dense(1, activation=keras.activations.linear)(self.denseV)
        self.Vmodel = keras.Model(inputs=[self.conv_model.input, self.dense_model.input],
                                  outputs=self.V, name='V-Model')

        self.noiseA = NoisyDense(100)

        self.denseA = self.noiseA(self.concat)
        self.denseA = keras.layers.ReLU()(self.denseA)
        self.A = keras.layers.Dense(881, activation=keras.activations.linear)(self.denseA)
        self.Amodel = keras.Model(inputs=[self.conv_model.input, self.dense_model.input],
                                  outputs=self.A, name='A-Model')

    def call(self, inputs, training=None, mask=None):
        V = self.Vmodel(inputs)
        A = self.Amodel(inputs)
        Q = V + A - tf.reduce_mean(A)
        return Q

    def reset_noise(self):
        self.noiseA.reset_noise()
        self.noiseV.reset_noise()

