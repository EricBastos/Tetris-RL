import os
import pygame
from .tile import Tile
import numpy as np


class Board(pygame.sprite.Sprite):

    matrix = np.array([
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'B'],
        ['B', 'E', 'E', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'B'],
        ['B', 'E', 'E', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'B'],
        ['B', 'E', 'E', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'B'],
        ['B', 'E', 'E', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'B'],
        ['B', 'E', 'E', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'J', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
    ])

    tile_lib = {
        'B': 'tetris/images/tiles/board_tile.png',
        'E': 'tetris/images/tiles/empty_tile.png',
        'I': 'tetris/images/tiles/i_tile.png',
        'J': 'tetris/images/tiles/j_tile.png',
        'L': 'tetris/images/tiles/l_tile.png',
        'O': 'tetris/images/tiles/o_tile.png',
        'S': 'tetris/images/tiles/s_tile.png',
        'T': 'tetris/images/tiles/t_tile.png',
        'Z': 'tetris/images/tiles/z_tile.png'
    }

    shadow_tile_lib = {
        'B': 'tetris/images/tiles/board_tile.png',
        'E': 'tetris/images/tiles/empty_tile.png',
        'I': 'tetris/images/tiles/i_tile_shadow.png',
        'J': 'tetris/images/tiles/j_tile_shadow.png',
        'L': 'tetris/images/tiles/l_tile_shadow.png',
        'O': 'tetris/images/tiles/o_tile_shadow.png',
        'S': 'tetris/images/tiles/s_tile_shadow.png',
        'T': 'tetris/images/tiles/t_tile_shadow.png',
        'Z': 'tetris/images/tiles/z_tile_shadow.png'
    }

    def __init__(self, position, settings, screen):
        super().__init__()
        self.board = pygame.sprite.Group()
        self.position = position
        self.settings = settings
        self.screen = screen
        self.recreate_board()

    def recreate_board(self):
        self.board.empty()
        for i in range(41):
            for j in range(12):
                new_tile = Tile(self.tile_lib['E'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                if self.matrix[i, j] == 'I':
                    new_tile = Tile(self.tile_lib['I'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i, j] == 'J':
                    new_tile = Tile(self.tile_lib['J'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i, j] == 'L':
                    new_tile = Tile(self.tile_lib['L'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i, j] == 'O':
                    new_tile = Tile(self.tile_lib['O'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i, j] == 'S':
                    new_tile = Tile(self.tile_lib['S'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i, j] == 'T':
                    new_tile = Tile(self.tile_lib['T'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i, j] == 'Z':
                    new_tile = Tile(self.tile_lib['Z'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i, j] == 'B':
                    new_tile = Tile(self.tile_lib['B'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                self.board.add(new_tile)

    def update(self):
        self.board.draw(self.screen)

    def change(self, tile, new_tile_name):
        self.matrix[tile[0], tile[1]] = new_tile_name
        self.board.sprites()[12*tile[0]+tile[1]].change_tile(self.tile_lib[new_tile_name])

# Line clear count (int)
# Perfect Clear (flag)
# T-spin (flag)

    def clear_lines(self, tile_name, tile_position, tile_rotation, last_movement, last_wallkick) -> [int, bool, bool]:
        cleared_lines = 0
        new_board = None
        last_cleared_line = 0
        perfect_clear = True
        tspin = False
        for i in range(19, 40):
            line_complete = True
            for j in range(1, 11):
                if self.matrix[i, j] == 'E':
                    line_complete = False
                    break
            if line_complete:
                cleared_lines += 1
                if new_board is not None:
                    new_board = np.vstack((new_board, self.matrix[last_cleared_line:i]))
                else:
                    new_board = self.matrix[last_cleared_line:i]
                last_cleared_line = i + 1
        if cleared_lines > 0:
            if new_board is not None:
                new_board = np.vstack((new_board, self.matrix[last_cleared_line:41]))
            for new_line in range(cleared_lines):
                new_board = np.vstack((np.array(['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B']), new_board))

            # Check Perfect Clear
            for i in reversed(range(40)):
                for j in range(1, 11):
                    if new_board[i, j] != 'E':
                        perfect_clear = False

            # Check T-spin
            if tile_name == 'T' and (last_movement == 'Rotate CClockwise' or last_movement == 'Rotate Clockwise'):
                if tile_rotation == 0:
                    if (self.matrix[tile_position[0], tile_position[1]] != 'E' and
                        self.matrix[tile_position[0], tile_position[1]+2] != 'E' and
                        (self.matrix[tile_position[0]+2, tile_position[1]] != 'E' or
                         self.matrix[tile_position[0]+2, tile_position[1]+2] != 'E')):
                        tspin = True
                elif tile_rotation == 1:
                    if (self.matrix[tile_position[0], tile_position[1]+2] != 'E' and
                        self.matrix[tile_position[0]+2, tile_position[1]+2] != 'E' and
                        (self.matrix[tile_position[0], tile_position[1]] != 'E' or
                         self.matrix[tile_position[0]+2, tile_position[1]] != 'E')):
                        tspin = True
                elif tile_rotation == 2:
                    if (self.matrix[tile_position[0]+2, tile_position[1]] != 'E' and
                        self.matrix[tile_position[0]+2, tile_position[1]+2] != 'E' and
                        (self.matrix[tile_position[0], tile_position[1]] != 'E' or
                         self.matrix[tile_position[0], tile_position[1]+2] != 'E')):
                        tspin = True
                elif tile_rotation == 3:
                    if (self.matrix[tile_position[0], tile_position[1]] != 'E' and
                        self.matrix[tile_position[0]+2, tile_position[1]] != 'E' and
                        (self.matrix[tile_position[0], tile_position[1]+2] != 'E' or
                         self.matrix[tile_position[0]+2, tile_position[1]+2] != 'E')):
                        tspin = True
                elif last_wallkick == 4:
                    tspin = True

            self.matrix = new_board.copy()
            self.recreate_board() # needs to be optimized

        return [cleared_lines, perfect_clear, tspin]

