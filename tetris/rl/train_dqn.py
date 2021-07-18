import os
import matplotlib.pyplot as plt
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
if os.path.exists('tetris_weights.h5'):
    print('Loading weights from previous learning session.')
    agent.load("tetris_weights.h5")
else:
    print('No weights found from previous learning session.')
done = False
batch_size = 32  # batch size used for the experience replay
return_history = []
episode = 0
frame_counter = 0
for episodes in range(1, NUM_EPISODES + 1):

    state, action_list = env.reset()
    action, _, advantage_means = agent.select_action(state, action_list)
    cumulative_reward = 0.0
    for move in range(1, NUM_MOVES+1):
        #clock.tick(720)
        env.loop(pygame.event.get())
        frame_counter += 1
        next_state, reward, done, action_list = env.step(action)

        cumulative_reward = agent.gamma * cumulative_reward + reward
        if done:
            print("episode: {}/{}, move: {}, score: {:.6}, epsilon: {:.3}"
                  .format(episodes, NUM_EPISODES, move, cumulative_reward, agent.epsilon))
            break

        next_action, best_next_action, next_advantage_means = agent.select_action(next_state, action_list)

        agent.append_experience(state, action, advantage_means, reward,
                                next_state, best_next_action, next_advantage_means, done)

        state = next_state
        action = next_action

        agent.update_beta(frame_counter, 100000)
        # Accumulate reward

        pygame.display.update()
        # We only update the policy if we already have enough experience in memory
        if len(agent.replay_buffer) > 2 * batch_size:
            agent.replay(batch_size)
    return_history.append(cumulative_reward)
    agent.update_epsilon()
    # Every 10 episodes, update the plot for training monitoring
    if episodes % 10 == 0:
        plt.plot(return_history, 'b')
        plt.xlabel('Episode')
        plt.ylabel('Return')
        plt.show(block=False)
        plt.pause(0.1)
        plt.savefig('dqn_training.png', format='png')
        # Saving the model to disk
        agent.save("tetris_weights.h5")
plt.pause(1.0)
