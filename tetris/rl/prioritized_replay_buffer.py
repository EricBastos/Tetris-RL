import random

from replay_buffer import ReplayBuffer
from segment_tree import SumSegmentTree, MinSegmentTree
import numpy as np
from typing import List


class PrioritizedReplayBuffer(ReplayBuffer):

    def __init__(self, state_dim: int, size: int, batch_size: int = 32, alpha: float = 0.6):
        super(PrioritizedReplayBuffer, self).__init__(state_dim, size, batch_size)
        self.max_priority = 1.0
        self.tree_ptr = 0
        self.alpha = alpha

        tree_capacity = 1
        while tree_capacity <= self.max_size:
            tree_capacity *= 2

        self.sum_tree = SumSegmentTree(tree_capacity)
        self.min_tree = MinSegmentTree(tree_capacity)

    def store(self, state_action: np.ndarray, reward: float, best_next_state_action: np.ndarray, done: bool):
        super(PrioritizedReplayBuffer, self).store(state_action, reward, best_next_state_action, done)

        self.sum_tree[self.tree_ptr] = self.max_priority ** self.alpha
        self.min_tree[self.tree_ptr] = self.max_priority ** self.alpha
        self.tree_ptr = (self.tree_ptr + 1) % self.max_size

    def sample_batch(self, beta: float = 0.4):
        assert len(self) >= self.batch_size
        idxs = self._sample_proportional()
        state_actions = np.array(self.state_action[idxs])
        rewards = np.array(self.rewards_buffer[idxs])
        best_next_state_action = np.array(self.best_next_state_action[idxs])
        done_buffer = np.array(self.done_buffer[idxs])
        ws = np.array([self._calculate_weight(i, beta) for i in idxs])
        return dict(state_actions=state_actions,
                    rewards=rewards,
                    best_next_state_actions=best_next_state_action,
                    dones=done_buffer,
                    weights=ws,
                    idxs=idxs)

    def update_priorities(self, idxs: List[int], priorities: np.ndarray):
        assert len(idxs) == len(priorities)

        for idx, priority in zip(idxs, priorities):
            self.sum_tree[idx] = priority ** self.alpha
            self.min_tree[idx] = priority ** self.alpha

            self.max_priority = max(self.max_priority, priority)

    def _sample_proportional(self):
        idxs = []
        total_p = self.sum_tree.sum(0, len(self)-1)
        segment = total_p / self.batch_size # When sampling batches

        for i in range(self.batch_size):
            a = segment * i
            b = segment * (i+1)
            upperbound = random.uniform(a, b)
            idx = self.sum_tree.find_prefixsum_idx(upperbound)
            idxs.append(idx)

        return idxs

    def _calculate_weight(self, idx: int, beta: float):
        p_min = self.min_tree.min() / self.sum_tree.sum()
        max_weight = (p_min * len(self)) ** (-beta)

        p_sample = self.sum_tree[idx] / self.sum_tree.sum()
        w = (p_sample * len(self)) ** (-beta)
        w = w / max_weight

        return w
