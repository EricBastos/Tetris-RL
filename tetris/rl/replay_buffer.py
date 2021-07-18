import numpy as np
from typing import Dict, List, Tuple


class ReplayBuffer:

    def __init__(self, state_dim: int, size: int, batch_size: int = 32):
        self.state_action = np.zeros([size, state_dim], dtype=np.float32)
        self.best_next_state_action = np.zeros([size, state_dim], dtype=np.float32)
        self.rewards_buffer = np.zeros([size], dtype=np.float32)
        self.done_buffer = np.zeros(size, dtype=np.float32)
        self.max_size, self.batch_size = size, batch_size
        self.ptr, self.size = 0, 0

    def store(self, state_action: np.ndarray, reward: float, best_next_state_action: np.ndarray, done: bool):
        self.state_action[self.ptr] = state_action
        self.rewards_buffer[self.ptr] = reward
        self.best_next_state_action[self.ptr] = best_next_state_action
        self.done_buffer[self.ptr] = done
        self.ptr = (self.ptr + 1) % self.max_size
        self.size = min(self.size + 1, self.max_size)

    def sample_batch(self):
        idxs = np.random.choice(self.size, size=self.batch_size, replace=False)
        state_actions = np.array(self.state_action[idxs])
        rewards = np.array(self.rewards_buffer[idxs])
        best_next_state_action = np.array(self.best_next_state_action[idxs])
        done_buffer = np.array(self.done_buffer[idxs])
        return dict(state_actions=state_actions,
                    rewards=rewards,
                    best_next_state_actions=best_next_state_action,
                    dones=done_buffer)

    def __len__(self):
        return self.size
