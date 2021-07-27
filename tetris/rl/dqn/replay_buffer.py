import numpy as np
from typing import Dict, List, Tuple


class ReplayBuffer:

    def __init__(self, size: int, batch_size: int = 32):
        self.matrix_buffer = np.zeros([size, 20, 10, 1], dtype=np.float32)
        self.pieces_buffer = np.zeros([size, 7], dtype=np.float32)
        self.action_buffer = np.zeros([size, 3], dtype=np.float32)
        self.next_matrix_buffer = np.zeros([size, 20, 10, 1], dtype=np.float32)
        self.next_pieces_buffer = np.zeros([size, 7], dtype=np.float32)
        self.rewards_buffer = np.zeros(size, dtype=np.float32)
        self.done_buffer = np.zeros(size, dtype=np.float32)
        self.next_mask_buffer = np.zeros([size, 881], dtype=np.float32)
        self.max_size, self.batch_size = size, batch_size
        self.ptr, self.size = 0, 0

    def store(self, matrix: np.ndarray, piece: np.ndarray, action: np.ndarray,
              reward: float, next_matrix: np.ndarray, next_piece: np.ndarray,
              done: bool, next_mask: np.ndarray):
        self.matrix_buffer[self.ptr] = matrix
        self.pieces_buffer[self.ptr] = piece
        self.next_matrix_buffer[self.ptr] = next_matrix
        self.next_pieces_buffer[self.ptr] = next_piece
        self.action_buffer[self.ptr] = action
        self.rewards_buffer[self.ptr] = reward
        self.done_buffer[self.ptr] = done
        self.next_mask_buffer[self.ptr] = next_mask
        self.ptr = (self.ptr + 1) % self.max_size
        self.size = min(self.size + 1, self.max_size)

    def sample_batch(self):
        idxs = np.random.choice(self.size, size=self.batch_size, replace=False)
        matrix = np.array(self.matrix_buffer[idxs])
        pieces = np.array(self.pieces_buffer[idxs])
        actions = np.array(self.action_buffer[idxs])
        rewards = np.array(self.rewards_buffer[idxs])
        next_matrix = np.array(self.next_matrix_buffer[idxs])
        next_pieces = np.array(self.next_pieces_buffer[idxs])
        done_buffer = np.array(self.done_buffer[idxs])
        next_mask_buffer = np.array(self.next_mask_buffer[idxs])
        return dict(matrixes=matrix,
                    pieces=pieces,
                    actions=actions,
                    rewards=rewards,
                    next_matrixes=next_matrix,
                    next_pieces=next_pieces,
                    dones=done_buffer,
                    next_masks=next_mask_buffer)

    def __len__(self):
        return self.size
