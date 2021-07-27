import os
import matplotlib.pyplot as plt
from tensorflow.python.ops.numpy_ops import np_config
import numpy as numpy
from ppo_agent import PPOAgent
from tetris import settings
from tetris.gamemodes import TetrisMode
import pygame

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))

pygame.display.set_caption(settings.TITLE)

env = TetrisMode(screen, settings)

# Creating the DQN agent
agent = PPOAgent()

# Checking if weights from previous learning session exists
if os.path.exists('tetris_weights_ppo.h5'):
    print('Loading weights from previous learning session.')
    agent.load("tetris_weights_ppo.h5")
else:
    print('No weights found from previous learning session.')

score_history = []
NUM_EPISODES = 50000
NUM_MOVES = 500
frame_counter = 0
for episodes in range(1, NUM_EPISODES + 1):

    state, _ = env.reset('ppo')
    score = 0
    for move in range(1, NUM_MOVES+1):
        action, action_num = agent.select_action(state)
        #print(action)
        env.loop(pygame.event.get())
        frame_counter += 1
        next_state, reward, done, _ = env.step(action, 'ppo')
        agent.append_experience(state, action_num, reward)
        score += reward

        pygame.display.update()

        if done:
            #print('broke')
            break

        state = next_state

    score_history.append(score)

    agent.learn()

    print("episode: {}/{}, move: {}, score_avg: {:.6}"
          .format(episodes, NUM_EPISODES, move, numpy.mean(score_history[-100:])))

    # Every 10 episodes, update the plot for training monitoring
    if episodes % 10 == 0:
        plt.plot(score_history, 'b')
        plt.xlabel('Episode')
        plt.ylabel('Return')
        try:
            plt.savefig('dqn_training_ppo.png', format='png')
        except OSError:
            continue
        # Saving the model to disk
        agent.save("tetris_weights_ppo.h5")