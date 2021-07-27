from keras import initializers
import tensorflow as tf

# Adapted From https://github.com/chucnorrisful/dqn


class NoisyDense(tf.keras.layers.Layer):
    def __init__(self, units):
        super(NoisyDense, self).__init__()
        self.units = units

    def build(self, input_shape):
        self.input_dim = input_shape[-1]
        self.kernel = self.add_weight(shape=(self.input_dim, self.units),
                                    initializer=initializers.RandomNormal(stddev=0.01),
                                    name='kernel',
                                    regularizer=None,
                                    constraint=None)

        self.kernel_sigma = self.add_weight(shape=(self.input_dim, self.units),
                                          initializer=initializers.Constant(0.017),
                                          name='sigma_kernel',
                                          regularizer=None,
                                          constraint=None)

        self.bias = self.add_weight(shape=(self.units,),
                                      initializer=initializers.RandomNormal(stddev=0.01),
                                      name='bias',
                                      regularizer=None,
                                      constraint=None)

        self.bias_sigma = self.add_weight(shape=(self.units,),
                                            initializer=initializers.Constant(0.017),
                                            name='bias_sigma',
                                            regularizer=None, constraint=None)
        self.reset_noise()

    def call(self, inputs, *args, **kwargs):
        return tf.matmul(inputs, self.kernel + tf.multiply(self.kernel_sigma, self.kernel_epsilon)) + \
               (self.bias + tf.multiply(self.bias_sigma, self.bias_epsilon))

    def reset_noise(self):
        self.kernel_epsilon = tf.random.uniform(shape=(self.input_dim, self.units))
        self.bias_epsilon = tf.random.uniform(shape=(self.units,))