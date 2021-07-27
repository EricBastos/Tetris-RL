import os
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.python.ops.numpy_ops import np_config

from dqn_agent import DQNAgent
from tetris import settings
from tetris.gamemodes import TetrisMode
import pygame

np_config.enable_numpy_behavior()

NUM_EPISODES = 100000
NUM_MOVES = 600
fig_format = 'png'

# Comment this line to enable training using your GPU
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#keras.backend.set_learning_phase(0) no teste

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))

pygame.display.set_caption(settings.TITLE)

env = TetrisMode(screen, settings)

# Creating the DQN agent
agent = DQNAgent()

# Checking if weights from previous learning session exists
if os.path.exists('tetris_weights_dqn.h5'):
    print('Loading weights from previous learning session.')
    agent.load("tetris_weights_dqn.h5")
else:
    print('No weights found from previous learning session.')
done = False
batch_size = 32  # batch size used for the experience replay
return_history = []
episode = 0
frame_counter = 0
for episodes in range(1, NUM_EPISODES + 1):

    state, _ = env.reset('ppo')
    cumulative_reward = 0.0
    for move in range(1, NUM_MOVES+1):
        #clock.tick(720)
        matrix, pieces, mask = state
        merged_state = [matrix[np.newaxis], pieces[np.newaxis]]
        action = agent.select_action(merged_state, mask)
        frame_counter += 1
        next_state, reward, done, _ = env.step(action, 'ppo')

        next_matrix, next_pieces, next_mask = next_state
        agent.append_experience(matrix, pieces, action, reward, next_matrix, next_pieces, done, next_mask)

        state = next_state
        env.loop(pygame.event.get())
        agent.update_beta(frame_counter, 100000)
        # Accumulate reward

        pygame.display.update()

        cumulative_reward = agent.gamma * cumulative_reward + reward

        if done:
            print("episode: {}/{}, move: {}, score: {:.6}"
                  .format(episodes, NUM_EPISODES, move, cumulative_reward))
            break

        # We only update the policy if we already have enough experience in memory
        if len(agent.replay_buffer) > 2 * batch_size:
            agent.replay()
    return_history.append(cumulative_reward)
    #agent.update_epsilon()
    # Every 10 episodes, update the plot for training monitoring
    if episodes % 10 == 0:
        plt.plot(return_history, 'b')
        plt.xlabel('Episode')
        plt.ylabel('Return')
        try:
            plt.savefig('dqn_training_dqn.png', format='png')
        except OSError:
            continue
        # Saving the model to disk
        agent.save("tetris_weights_dqn.h5")
plt.pause(1.0)
