import random

from tetris.gamemodes.tetris import TetrisMode

env = TetrisMode()

run = True
while run:
    actions = env.reset()
    act = random.sample(actions, 1)[0]
    while True:
        state_matrix, line_info, pieces, moves, done = env.step(act)
        env.render()
        if done:
            break
        act = random.sample(moves, 1)[0]


