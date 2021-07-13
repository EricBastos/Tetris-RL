from .gamemode import GameMode
import pygame
from ..tiles import Board, Tetromino, Tile
import random


class TetrisMode(GameMode):

    def __init__(self, screen, settings):
        super().__init__(screen, settings)
        self.screen = screen
        self.board_position = pygame.Vector2((settings.screen_width - settings.board_width) / 2 - settings.tile_size,
                                        (-settings.tile_size * 41) + settings.screen_height)
        self.board = Board(self.board_position, settings, screen)
        self.next_pieces = pygame.sprite.Group()
        self.hold_piece = pygame.sprite.Group()
        self.hold_tetromino = ''
        self.has_held = False
        self.current_tetromino = None
        self.current_bag_index = 0
        self.current_bag = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        self.next_bag = self.current_bag
        random.shuffle(self.current_bag)
        random.shuffle(self.next_bag)
        self.generate_tetromino()
        self.evaluate_next_pieces()

    def loop(self, events):
        for event in events:
            if event.type == pygame.USEREVENT+1:
                self.tile_placed(event.tileList, event.tileName)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    self.hold()

        self.screen.fill(0)
        self.board.update()
        self.current_tetromino.update(events)
        self.next_pieces.draw(self.screen)
        self.hold_piece.draw(self.screen)

    def tile_placed(self, tile_list, tile_name):
        for tile in tile_list:
            self.board.change(tile, tile_name)

        self.generate_tetromino()
        self.evaluate_next_pieces()
        self.has_held = False

    def generate_tetromino(self):
        if self.current_bag_index == 7:
            self.current_bag = self.next_bag.copy()
            random.shuffle(self.next_bag)
            self.current_bag_index = 0

        self.current_tetromino = Tetromino(self.board, self.current_bag[self.current_bag_index],
                                           self.board_position, self.settings, self.screen)
        self.current_bag_index += 1

    def evaluate_next_pieces(self):
        self.next_pieces.empty()
        all_pieces = self.current_bag+self.next_bag
        print(all_pieces)
        draw_position = pygame.Vector2(self.settings.screen_width/2 + 8*self.settings.tile_size, 1*self.settings.tile_size)
        for i in range(self.current_bag_index, self.current_bag_index+5):
            tile_name = all_pieces[i]
            data = Tetromino.tetromino_lib[tile_name][0]
            xoffset = 0
            if tile_name == 'I' or tile_name == 'O':
                xoffset = -self.settings.tile_size/2
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if data[i][j] != 0:
                        new_tile = Tile(self.board.tile_lib[tile_name],
                                        draw_position + pygame.Vector2(j * self.settings.tile_size+xoffset,
                                                                       i * self.settings.tile_size))
                        self.next_pieces.add(new_tile)
            draw_position += pygame.Vector2(0, 3*self.settings.tile_size)

    def hold(self):
        if not self.has_held:
            self.has_held = True
            self.current_tetromino.kill()
            if self.hold_tetromino == '':
                self.hold_tetromino = self.current_tetromino.name
                self.generate_tetromino()
            else:
                temp_hold_name = self.hold_tetromino
                self.hold_tetromino = self.current_tetromino.name
                self.current_tetromino = Tetromino(self.board, temp_hold_name,
                                                   self.board_position, self.settings, self.screen)
            draw_position = pygame.Vector2(self.settings.screen_width / 2 - 11 * self.settings.tile_size,
                                           1 * self.settings.tile_size)
            self.hold_piece.empty()
            data = Tetromino.tetromino_lib[self.hold_tetromino][0]
            xoffset = 0
            if self.hold_tetromino == 'I' or self.hold_tetromino == 'O':
                xoffset = -self.settings.tile_size / 2
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if data[i][j] != 0:
                        new_tile = Tile(self.board.tile_lib[self.hold_tetromino],
                                        draw_position + pygame.Vector2(j * self.settings.tile_size + xoffset,
                                                                       i * self.settings.tile_size))
                        self.hold_piece.add(new_tile)
