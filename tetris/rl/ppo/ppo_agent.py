import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.optimizers import Adam
import numpy as np
from ppo_network import PPONetwork


class PPOAgent:
    def __init__(self, lr=1e-5, gamma=0.99):
        self.gamma = gamma
        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []
        self.policy = PPONetwork()
        self.policy.build([(None, 20, 10, 1), (None, 7)])
        self.policy.summary()
        self.policy.compile(optimizer=Adam(learning_rate=lr))

    def select_action(self, state):
        matrix_batch = []
        pieces_batch = []
        mask_batch = []
        matrix_batch.append(state[0])
        matrix_batch = np.array(matrix_batch)
        pieces_batch.append(state[1])
        pieces_batch = np.array(pieces_batch)
        mask_batch.append(state[2])
        mask_batch = np.array(mask_batch)
        prob_dist = self.policy([matrix_batch, pieces_batch])
        prob_dist = tf.multiply(prob_dist, mask_batch)
        prob_dist = prob_dist / tf.reduce_mean(prob_dist)
        action_probs = tfp.distributions.Categorical(probs=prob_dist)
        action = action_probs.sample()
        action_num = action.numpy()[0]
        #print(f'{action_num} {mask_batch[0][action_num]}')
        rotation = 0
        while action >= 220:
            action -= 220
            rotation += 1
        line = 0
        while action >= 11:
            action -= 11
            line += 1
        column = action.numpy()[0]
        #print(f'{line+20} {column+1} {rotation}')
        return [line+20, column-1, rotation], action_num

    def append_experience(self, state, action, reward):
        self.state_memory.append(state)
        self.action_memory.append(action)
        self.reward_memory.append(reward)

    def learn(self):
        actions = tf.convert_to_tensor(self.action_memory, dtype=tf.float32)
        rewards = tf.convert_to_tensor(self.reward_memory, dtype=tf.float32)

        G = np.zeros_like(rewards)
        for t in range(len(rewards)):
            G_sum = 0
            discount = 1
            for k in range(t, len(rewards)):
                G_sum += rewards[k] * discount
                discount *= self.gamma
            G[t] = G_sum

        with tf.GradientTape() as tape:
            loss = 0
            for idx, (g, state) in enumerate(zip(G, self.state_memory)):
                matrix_batch = []
                pieces_batch = []
                matrix_batch.append(state[0])
                matrix_batch = np.array(matrix_batch)
                pieces_batch.append(state[1])
                pieces_batch = np.array(pieces_batch)
                prob_dist = self.policy([matrix_batch, pieces_batch])
                action_probs = tfp.distributions.Categorical(probs=prob_dist)
                log_prob = action_probs.log_prob(actions[idx])
                loss += -g * tf.squeeze(log_prob)
                #print(loss)
        gradient = tape.gradient(loss, self.policy.trainable_variables)
        print(gradient)
        self.policy.optimizer.apply_gradients(zip(gradient, self.policy.trainable_variables))

        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []

    def load(self, name):

        self.policy.load_weights(name)

    def save(self, name):

        self.policy.save_weights(name)