import numpy as np
import numpy.ma as ma
from keras import models, layers, optimizers, activations, losses
from prioritized_replay_buffer import PrioritizedReplayBuffer
from dueling_dqn import DuelingDQN
import tensorflow as tf


def _huber_loss(loss):
    return 0.5 * loss ** 2 if np.abs(loss) < 1.0 else np.abs(loss) - 0.5


def _decode_action(q_index):
    rotation = 0
    while q_index >= 220:
        q_index -= 220
        rotation += 1
    line = 0
    while q_index >= 11:
        q_index -= 11
        line += 1
    column = q_index
    return [line + 20, column - 1, rotation]


class DQNAgent:
    """
    Represents a Deep Q-Networks (DQN) agent.
    """

    def __init__(self, gamma=0.99, epsilon=0.8, epsilon_min=0.01,
                 epsilon_decay=0.998, learning_rate=1e-4,
                 target_count=500, alpha=0.2, beta=0.6, buffer_epsilon=1e-6):

        self.beta = beta  # Beta for PER
        self.buffer_epsilon = buffer_epsilon  # Min td error to guarantee every experience has a chance
        self.replay_buffer = PrioritizedReplayBuffer(2048, batch_size=32, alpha=alpha)  # PER

        self.gamma = gamma  # For Q learning
        self.epsilon = epsilon  # Epsilon-greedy action policy
        self.epsilon_min = epsilon_min  # Minimum epsilon
        self.epsilon_decay = epsilon_decay  # Value to decay epsilon after each update

        self.learning_rate = learning_rate  # Optimizer learning rate
        self.target_count = target_count  # Number of frames before updating target network
        self.update_count = 0  # Current frame

        # Custom Dueling networks
        self.model = DuelingDQN()  # DQN Network
        self.target_network = DuelingDQN()  # DDQN Network (Target)

        self.model.build([(None, 20, 10, 1), (None, 7)])  # Build custom network
        self.target_network.build([(None, 20, 10, 1), (None, 7)])
        self.model.compile(loss=losses.Huber(), optimizer=optimizers.Adam(learning_rate=self.learning_rate))
        self.model.summary()
        #self.model.Amodel.summary()
        #self.model.Vmodel.summary()
    def select_action(self, state, mask):
        # print(state[0].shape)
        # Since the action space is variable, we concatenate v=(s,a) to evaluate Q(v)
        Qs = self.model(state, training=False)[0]  # Predict Advantage for each action
        mx = ma.masked_array(Qs, mask=mask)
        #mx_index = ma.masked_array(np.arange(len(Qs)), mask=mask).compressed()
        best_action_index = np.argmax(mx)  # Choose the best action
        best_action = _decode_action(best_action_index)
        #p = np.random.rand(1)  # Select action according to epsilon-greedy policy
        #if p < 1 - self.epsilon:
        selected_action = best_action
        #else:
        #    selected_index = np.random.choice(mx_index)
        #    selected_action = _decode_action(selected_index)

        return selected_action  # Return selected and best action (best action later for DDQN)

    def append_experience(self, matrix, piece, action, reward,
                          next_matrix, next_piece, done, next_mask):

        # Store experience (note that we need best_next_action for DDQN)
        self.replay_buffer.store(matrix, piece, action, reward,
                                 next_matrix, next_piece, done, next_mask)

    def replay(self):

        # Update target network if it's time
        if self.update_count == 0:
            self.target_network.set_weights(self.model.get_weights())
            print('Updating target')

        # Using prioritized experience replay
        minibatch = self.replay_buffer.sample_batch()

        # Weights and indices for each experience in batch
        ws = minibatch['weights'].reshape((-1, 1))
        idxs = minibatch['idxs']

        # Experience info
        matrixes = minibatch['matrixes'].reshape((-1, 20, 10, 1))
        pieces = minibatch['pieces'].reshape((-1, 7))
        rewards = minibatch['rewards'].reshape((-1, 1))
        actions = minibatch['actions'].reshape((-1, 3))
        next_matrixes = minibatch['next_matrixes'].reshape((-1, 20, 10, 1))
        next_pieces = minibatch['next_pieces'].reshape((-1, 7))
        dones = minibatch['dones'].reshape((-1, 1))
        masks = minibatch['next_masks'].reshape((-1, 881))

        # Gamma vector according to done vector
        gammas = np.reshape(self.gamma * (1 - dones), (-1, 1))

        # Fixed Q target: use target_network to evaluate Q(s_{t+1},a_{t+1})
        # DDQN: a_{t+1} is evaluated from DQN and used on target_network
        future_rewards = self.target_network([next_matrixes, next_pieces], training=False)
        evaluate_next_state = self.model([next_matrixes, next_pieces], training=False)
        mx = ma.masked_array(evaluate_next_state, mask=masks)
        best_next_action_index = np.argmax(mx, axis=1).reshape(-1, 1)  # Choose the best action
        best_next_q = np.take_along_axis(future_rewards, best_next_action_index, axis=1)
        updated_q = rewards + np.multiply(gammas, best_next_q)
        encoded_actions = (220 * actions[:, 2] + 11 * (actions[:, 0] - 20) + actions[:, 1] + 1).astype(
            np.int32).reshape(-1, 1)

        with tf.GradientTape() as tape:
            q_values = self.model([matrixes, pieces], training=True)
            q_action = tf.experimental.numpy.take_along_axis(q_values, encoded_actions, axis=1)
            elementwise_loss = losses.Huber(reduction='none')(updated_q, q_action, ws)
            loss = tf.reduce_mean(elementwise_loss)

        new_priorities = (elementwise_loss + self.buffer_epsilon).reshape(-1, 1)
        grads = tape.gradient(loss, self.model.trainable_variables)
        grads = [tf.clip_by_norm(g, 10) for g in grads]
        self.model.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        self.replay_buffer.update_priorities(idxs, new_priorities)

        # Update count for target network
        self.update_count = (self.update_count + 1) % self.target_count
        # Reset Noise
        self.model.reset_noise()
        self.target_network.reset_noise()

        return loss

    def load(self, name):

        self.model.load_weights(name)
        self.target_network.load_weights(name)

    def save(self, name):

        self.model.save_weights(name)

    def update_epsilon(self):
        """
        Updates the epsilon used for epsilon-greedy action selection.
        """
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min

    def update_beta(self, current_frame, max_frames):
        fraction = min(current_frame / max_frames, 1.0)
        self.beta = self.beta + fraction * (1.0 - self.beta)
