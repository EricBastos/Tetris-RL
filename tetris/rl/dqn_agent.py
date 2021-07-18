import random

import keras
import numpy as np
from keras import models, layers, optimizers, activations, losses
from prioritized_replay_buffer import PrioritizedReplayBuffer
from dueling_dqn import DuelingDQN


def _huber_loss(loss):
    return 0.5 * loss ** 2 if np.abs(loss) < 1.0 else np.abs(loss) - 0.5


class DQNAgent:
    """
    Represents a Deep Q-Networks (DQN) agent.
    """

    def __init__(self, gamma=0.99, epsilon=0.5, epsilon_min=0.01,
                 epsilon_decay=0.985, learning_rate=0.0005,
                 target_count=500, alpha=0.2, beta=0.6, buffer_epsilon=1e-6):

        self.state_size = 31    # Matrix and pieces (bitstream to 28 uint8) + action (3 bytes)
        self.action_size = 1    # Q(s,a)

        self.beta = beta    # Beta for PER
        self.buffer_epsilon = buffer_epsilon    # Min td error to guarantee every experience has a chance
        self.replay_buffer = PrioritizedReplayBuffer(self.state_size, 6144, batch_size=32, alpha=alpha) # PER

        self.gamma = gamma  # For Q learning
        self.epsilon = epsilon  # Epsilon-greedy action policy
        self.epsilon_min = epsilon_min  # Minimum epsilon
        self.epsilon_decay = epsilon_decay  # Value to decay epsilon after each update

        self.learning_rate = learning_rate  # Otimizer learning rate
        self.target_count = target_count    # Number of frames before updating target network
        self.update_count = 0   # Current frame

        # Custom Dueling networks
        self.model = DuelingDQN()  # DQN Network
        self.target_network = DuelingDQN()  # DDQN Network (Target)
        self.model.build((None, self.state_size))   # Build custom network
        self.target_network.build((None, self.state_size))
        self.model.compile(loss=losses.Huber(), optimizer=optimizers.Adam(learning_rate=self.learning_rate))

        self.model.summary()

    # In case we don't want Dueling networks
    def make_model(self):

        model = models.Sequential()
        model.add(layers.Dense(100, activation=activations.linear, input_dim=self.state_size))
        model.add(layers.Dense(50, activation=activations.relu))
        model.add(layers.Dense(10, activation=activations.relu))
        model.add(layers.Dense(self.action_size, activation=activations.linear))

        model.compile(loss=losses.Huber(),
                      optimizer=optimizers.Adam(learning_rate=self.learning_rate))
        model.summary()
        return model

    def select_action(self, state, action_list):

        # Since the action space is variable, we concatenate v=(s,a) to evaluate Q(v)
        state_action_batch = []
        for i in range(len(action_list)):
            state_action = np.array([np.concatenate((state, np.hstack(action_list[i])))])
            state_action_batch.append(state_action[0])

        Advantages = self.model.advantage(np.array(state_action_batch))   # Predict Advantage for each action
        advantages_mean = np.mean(Advantages)   # Evaluate mean of advantages

        Qs = self.model(np.array(state_action_batch))   # Choose action according to Q
        best_action = action_list[np.argmax(Qs)]    # Choose the best action
        p = np.random.rand(1)   # Select action according to epsilon-greedy policy
        if p < 1 - self.epsilon:
            selected_action = best_action
        else:
            selected_action = random.choice(action_list)

        return selected_action, best_action # Return selected and best action (best action later for DDQN)

    def append_experience(self, state, action, reward, next_state, best_next_action, done):

        # Store experience (note that we need best_next_action for DDQN)
        self.replay_buffer.store(np.array([np.concatenate((state, np.hstack(action)))]),
                                 reward,
                                 np.array([np.concatenate((next_state, np.hstack(best_next_action)))]),
                                 done)

    def replay(self, batch_size):

        # Update target network if it's time
        if self.update_count == 0:
            self.target_network.set_weights(self.model.get_weights())
            print('Updating target')

        # Using prioritized experience replay
        minibatch = self.replay_buffer.sample_batch()

        # Weights and indices for each experience in batch
        ws = minibatch['weights'].reshape(-1, 1)
        idxs = minibatch['idxs']

        # Experience info
        state_actions = minibatch['state_actions'].reshape(-1, self.state_size)
        rewards = minibatch['rewards'].reshape(-1, 1)
        best_next_state_actions = minibatch['best_next_state_actions'].reshape(-1, self.state_size)
        dones = minibatch['dones'].reshape(-1, 1)

        # Gamma vector according to done vector
        gammas = np.reshape(self.gamma * (1-dones), (-1, 1))

        # Fixed Q target: use target_network to evaluate Q(s_{t+1},a_{t+1})
        # DDQN: a_{t+1} is evaluated from DQN and used on target_network
        targets = rewards + np.multiply(gammas, self.target_network(best_next_state_actions))

        # Train using batch
        history = self.model.fit(state_actions, targets, batch_size=batch_size, epochs=1, verbose=0, sample_weight=ws)

        # Calculate TD error and update PER priorities
        error = np.vectorize(_huber_loss)(targets - self.model(state_actions))
        new_priorities = np.array(error + self.buffer_epsilon)
        self.replay_buffer.update_priorities(idxs, new_priorities)

        # Update count for target network
        self.update_count = (self.update_count + 1) % self.target_count

        return history.history['loss'][0]

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

