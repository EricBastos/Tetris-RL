import os
import pygame
from .tile import Tile
import numpy as np


class Board(pygame.sprite.Sprite):

    matrix = [
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
        ['B', 'E', 'E', 'E', 'E', 'E', 'L', 'L', 'E', 'E', 'E', 'B'],
        ['B', 'E', 'E', 'E', 'E', 'E', 'L', 'L', 'E', 'E', 'I', 'B'],
        ['B', 'O', 'O', 'E', 'E', 'E', 'L', 'L', 'E', 'E', 'I', 'B'],
        ['B', 'O', 'O', 'E', 'E', 'S', 'L', 'L', 'E', 'E', 'I', 'B'],
        ['B', 'J', 'J', 'Z', 'E', 'S', 'S', 'E', 'E', 'E', 'I', 'B'],
        ['B', 'J', 'Z', 'Z', 'S', 'S', 'S', 'E', 'J', 'J', 'J', 'B'],
        ['B', 'J', 'Z', 'S', 'S', 'O', 'O', 'E', 'E', 'T', 'J', 'B'],
        ['B', 'I', 'I', 'I', 'I', 'O', 'O', 'E', 'T', 'T', 'T', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
    ]

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
                if self.matrix[i][j] == 'I':
                    new_tile = Tile(self.tile_lib['I'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i][j] == 'J':
                    new_tile = Tile(self.tile_lib['J'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i][j] == 'L':
                    new_tile = Tile(self.tile_lib['L'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i][j] == 'O':
                    new_tile = Tile(self.tile_lib['O'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i][j] == 'S':
                    new_tile = Tile(self.tile_lib['S'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i][j] == 'T':
                    new_tile = Tile(self.tile_lib['T'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i][j] == 'Z':
                    new_tile = Tile(self.tile_lib['Z'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                elif self.matrix[i][j] == 'B':
                    new_tile = Tile(self.tile_lib['B'], self.position + pygame.Vector2(j*self.settings.tile_size, i*self.settings.tile_size))
                self.board.add(new_tile)

    def update(self):
        self.board.draw(self.screen)

    def change(self, tile, new_tile_name) -> int:
        self.matrix[tile[0]][tile[1]] = new_tile_name
        self.board.sprites()[12*tile[0]+tile[1]].change_tile(self.tile_lib[new_tile_name])

        cleared_lines = 0
        for i in range(19,40):
            line_complete = True
            for j in range(1, 11):
                if self.matrix[i][j] == 'E':
                    line_complete = False
                    break
            if line_complete:
                cleared_lines += 1
                for lines_above in reversed(range(1, i+1)):
                    self.matrix[lines_above] = self.matrix[lines_above-1]
                self.matrix[0] = ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B']
        if cleared_lines > 0:
            self.recreate_board()
        return cleared_lines
