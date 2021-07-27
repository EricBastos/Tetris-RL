from abc import ABC

import tensorflow.keras as keras
from keras.layers import Dense, Conv2D, Lambda
from keras.models import Model


class PPONetwork(Model, ABC):
    def __init__(self):
        super(PPONetwork, self).__init__()

        self.input_conv = keras.layers.Input((20, 10, 1), name='Input-Conv')
        self.input_dense = keras.layers.Input(7, name='Input-Dense')
        #self.input_actionmask = keras.layers.Input(881, name='Input-Mask')

        self.conv1 = keras.layers.Conv2D(64, (20, 1), activation='relu')(self.input_conv)
        self.conv2 = keras.layers.Conv2D(32, (1, 4), activation='relu')(self.conv1)
        self.conv3 = keras.layers.Conv2D(16, (1, 7), activation='relu')(self.conv2)
        # self.pool1 = keras.layers.AvgPool2D((2, 2))(self.conv1)
        self.flatten1 = keras.layers.Flatten()(self.conv3)
        self.conv_model = keras.Model(inputs=self.input_conv, outputs=self.flatten1, name='Conv-Model')

        self.dense1 = keras.layers.Dense(20, activation='relu')(self.input_dense)
        self.dense2 = keras.layers.Dense(10, activation='relu')(self.dense1)
        self.dense_model = keras.Model(inputs=self.input_dense, outputs=self.dense2, name='Dense-Model')

        self.concat = keras.layers.concatenate([self.conv_model.output, self.dense_model.output])
        self.concat = keras.layers.BatchNormalization()(self.concat)

        self.densePolicy1 = keras.layers.Dense(64, activation='relu')(self.concat)
        self.policy = keras.layers.Dense(881, activation='softmax')(self.densePolicy1)

        self.model = keras.Model(inputs=[self.conv_model.input, self.dense_model.input],
                                 outputs=self.policy, name='Policy-Model')

    def call(self, inputs, training=None, mask=None):
        return self.model(inputs)
