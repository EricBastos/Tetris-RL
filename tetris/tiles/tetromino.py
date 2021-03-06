from .tile import Tile
import os
import pygame
import numpy as np


class Tetromino(pygame.sprite.Sprite):
    tetromino_lib = {
        'I': {
            0: [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
            1: [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
            2: [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
            3: [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]
        },
        'J': {
            0: [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
            1: [[0, 1, 1], [0, 1, 0], [0, 1, 0]],
            2: [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
            3: [[0, 1, 0], [0, 1, 0], [1, 1, 0]]
        },
        'L': {
            0: [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
            1: [[0, 1, 0], [0, 1, 0], [0, 1, 1]],
            2: [[0, 0, 0], [1, 1, 1], [1, 0, 0]],
            3: [[1, 1, 0], [0, 1, 0], [0, 1, 0]]
        },
        'O': {
            0: [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
            1: [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
            2: [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
            3: [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
        },
        'S': {
            0: [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
            1: [[0, 1, 0], [0, 1, 1], [0, 0, 1]],
            2: [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
            3: [[1, 0, 0], [1, 1, 0], [0, 1, 0]]
        },
        'T': {
            0: [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
            1: [[0, 1, 0], [0, 1, 1], [0, 1, 0]],
            2: [[0, 0, 0], [1, 1, 1], [0, 1, 0]],
            3: [[0, 1, 0], [1, 1, 0], [0, 1, 0]]
        },
        'Z': {
            0: [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
            1: [[0, 0, 1], [0, 1, 1], [0, 1, 0]],
            2: [[0, 0, 0], [1, 1, 0], [0, 1, 1]],
            3: [[0, 1, 0], [1, 1, 0], [1, 0, 0]]
        }
    }

    wall_kick = {
        'others': {
            1: [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
            10: [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
            12: [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
            21: [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
            23: [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
            32: [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
            30: [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
            3: [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
        },
        'I': {
            1: [(0, 0), (-2, 0), (1, -1), (-2, 1), (1, -2)],
            10: [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
            12: [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
            21: [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
            23: [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
            32: [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
            30: [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
            3: [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)]
        }
    }

    def __init__(self, board, name, board_position, settings, screen):
        super().__init__()
        self.board = board
        self.board_position = board_position
        self.name = name
        self.rotation = 0
        self.settings = settings
        self.debug_autoplay = settings.DEBUG_AUTOMOVE
        self.debug_shadow_line = 10
        self.debug_shadow_column = 10
        self.debug_shadow_rotation = 0
        self.tileset = pygame.sprite.Group()
        self.shadow = pygame.sprite.Group()
        self.screen = screen
        self.data = self.tetromino_lib[self.name]
        self.line = 19
        self.column = 4
        init_pos = self.board_position + pygame.Vector2(self.column * settings.tile_size,
                                                        self.line * settings.tile_size)
        for i in range(len(self.data[self.rotation])):
            for j in range(len(self.data[self.rotation][i])):
                if self.data[self.rotation][i][j] != 0:
                    new_tile = Tile(self.board.tile_lib[name],
                                    init_pos + pygame.Vector2(j * settings.tile_size, i * settings.tile_size))
                    self.tileset.add(new_tile)

        self.last_movement = 'Left'
        self.last_wallkick = 0
        self.calculate_shadow()

        self.DAS_counter = self.settings.DAS
        self.ARR_counter = 0
        self.lock_down = 0
        self.movement_count = 0

    def update(self, events):
        self.tileset.draw(self.screen)
        self.shadow.draw(self.screen)
        self.handle_input(events)
        if not self.debug_autoplay:
            self.handle_gravity()

    def handle_gravity(self):
        if self.lock_down == self.settings.TIME_DELAY:
            self.lock_down = 0
            if not self.check_collision(self.rotation, (0, 1)):
                self.line += 1
                for tile in self.tileset.sprites():
                    tile.update((tile.rect.x, tile.rect.y + self.settings.tile_size))
                self.calculate_shadow()
                self.last_movement = 'Down'
            else:
                self.lock_piece()
        else:
            self.lock_down += 1

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.DAS_counter = self.settings.DAS
                    if not self.check_collision(self.rotation, (-1, 0)):
                        self.column = self.column - 1
                        for tile in self.tileset.sprites():
                            tile.update((tile.rect.x - self.settings.tile_size, tile.rect.y))
                        self.calculate_shadow()
                        self.last_movement = 'Left'
                        if self.movement_count < self.settings.MAX_RESET and self.check_collision(self.rotation, (0, 1)):
                            self.lock_down = 0
                            self.movement_count += 1
                elif event.key == pygame.K_d:
                    self.DAS_counter = self.settings.DAS
                    if not self.check_collision(self.rotation, (1, 0)):
                        self.column += 1
                        for tile in self.tileset.sprites():
                            tile.update((tile.rect.x + self.settings.tile_size, tile.rect.y))
                        self.calculate_shadow()
                        self.last_movement = 'Right'
                        if self.movement_count < self.settings.MAX_RESET and self.check_collision(self.rotation, (0, 1)):
                            self.lock_down = 0
                            self.movement_count += 1
                elif event.key == pygame.K_s:
                    self.DAS_counter = self.settings.DAS
                    if not self.check_collision(self.rotation, (0, 1)):
                        self.line += 1
                        for tile in self.tileset.sprites():
                            tile.update((tile.rect.x, tile.rect.y + self.settings.tile_size))
                        self.calculate_shadow()
                        self.last_movement = 'Down'
                        self.lock_down = 0
                elif event.key == pygame.K_k or event.key == pygame.K_l:
                    rotation_change_value = -1
                    if event.key == pygame.K_l:
                        rotation_change_value = 1
                    temp_rotation = (self.rotation + rotation_change_value) % 4
                    rotation_key = self.rotation * 10 + temp_rotation
                    piece_key = 'others'
                    if self.name == 'I':
                        piece_key = 'I'
                    detected_collision = True
                    successful_test = None
                    for i in range(5):
                        #print(f'Walkick test {rotation_key} {piece_key} {i}')
                        if not self.check_collision(temp_rotation, self.wall_kick[piece_key][rotation_key][i]):
                            successful_test = i
                            detected_collision = False
                            break
                    if not detected_collision:
                        self.tileset.empty()
                        self.column += self.wall_kick[piece_key][rotation_key][successful_test][0]
                        self.line += self.wall_kick[piece_key][rotation_key][successful_test][1]
                        self.rotation = temp_rotation
                        pos = self.board_position + pygame.Vector2(self.column * self.settings.tile_size,
                                                                   self.line * self.settings.tile_size)
                        for i in range(len(self.data[self.rotation])):
                            for j in range(len(self.data[self.rotation][i])):
                                if self.data[self.rotation][i][j] != 0:
                                    new_tile = Tile(self.board.tile_lib[self.name],
                                                    pos + pygame.Vector2(j * self.settings.tile_size,
                                                                         i * self.settings.tile_size))
                                    self.tileset.add(new_tile)
                        self.last_wallkick = successful_test
                        self.calculate_shadow()
                        self.last_movement = "Rotate CClockwise"
                        if event.key == pygame.K_l:
                            self.last_movement = "Rotate Clockwise"
                        if self.movement_count < self.settings.MAX_RESET and self.check_collision(self.rotation, (0, 1)):
                            self.lock_down = 0
                            self.movement_count += 1
                elif event.key == pygame.K_SPACE:
                    self.lock_piece()

        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_d] or key[pygame.K_s]:
            if self.DAS_counter > 0:
                self.DAS_counter -= 1
            else:
                if self.ARR_counter > 0:
                    self.ARR_counter -= 1
                else:
                    self.ARR_counter = self.settings.ARR
                    if key[pygame.K_a]:
                        if not self.check_collision(self.rotation, (-1, 0)):
                            self.column = self.column - 1
                            for tile in self.tileset.sprites():
                                tile.update((tile.rect.x - self.settings.tile_size, tile.rect.y))
                            self.calculate_shadow()
                            self.last_movement = 'Left'
                    elif key[pygame.K_d]:
                        if not self.check_collision(self.rotation, (1, 0)):
                            self.column += 1
                            for tile in self.tileset.sprites():
                                tile.update((tile.rect.x + self.settings.tile_size, tile.rect.y))
                            self.calculate_shadow()
                            self.last_movement = 'Right'
                    else:
                        if not self.check_collision(self.rotation, (0, 1)):
                            self.line += 1
                            for tile in self.tileset.sprites():
                                tile.update((tile.rect.x, tile.rect.y + self.settings.tile_size))
                            self.calculate_shadow()
                            self.last_movement = 'Down'

    def check_collision(self, rotation, translation):
        for i in range(len(self.data[rotation])):
            for j in range(len(self.data[rotation][i])):
                if self.data[rotation][i][j] != 0:
                    try:
                        if self.board.matrix[self.line + translation[1] + i, self.column + translation[0] + j] != 'E':
                            return True
                    except (IndexError, ValueError):
                        return True
        return False

    def calculate_shadow(self):
        shadow_line = self.line
        shadow_column = self.column
        shadow_rotation = self.rotation

        current_line = self.line
        while not self.check_collision(shadow_rotation, (0, 1)):
            shadow_line += 1
            self.line += 1
        self.line = current_line
        if self.debug_autoplay:
            shadow_rotation = self.debug_shadow_rotation
            shadow_line = self.debug_shadow_line
            shadow_column = self.debug_shadow_column
        pos = self.board_position + pygame.Vector2(shadow_column * self.settings.tile_size,
                                                   shadow_line * self.settings.tile_size)
        self.shadow.empty()
        #if shadow_line is not self.line:
        for i in range(len(self.data[shadow_rotation])):
            for j in range(len(self.data[shadow_rotation][i])):
                if self.data[shadow_rotation][i][j] != 0:
                    new_tile = Tile(self.board.shadow_tile_lib[self.name],
                                    pos + pygame.Vector2(j * self.settings.tile_size, i * self.settings.tile_size))
                    self.shadow.add(new_tile)

    def lock_piece(self):
        line_dif = 0
        while not self.check_collision(self.rotation, (0, 1)):
            line_dif += 1
            self.line += 1
        tiles_to_append = []
        for i in range(len(self.data[self.rotation])):
            for j in range(len(self.data[self.rotation][i])):
                if self.data[self.rotation][i][j] != 0:
                    tiles_to_append.append((i + self.line, j + self.column))
        pygame.event.post(
            pygame.event.Event(pygame.USEREVENT + 1, tileList=tiles_to_append, tileName=self.name,
                               tilePos=(self.line, self.column), tileRotation=self.rotation,
                               lastMovement=self.last_movement, lastWallkick=self.last_wallkick))
        self.tileset.empty()
        self.shadow.empty()
        self.last_movement = 'Left'
        self.last_wallkick = 0

    def kill(self) -> None:
        super().kill()
        self.tileset.empty()
        self.shadow.empty()

    def restart_tile(self):
        self.tileset.empty()
        init_pos = self.board_position + pygame.Vector2(4 * self.settings.tile_size,
                                                        19 * self.settings.tile_size)
        for i in range(len(self.data[self.rotation])):
            for j in range(len(self.data[self.rotation][i])):
                if self.data[self.rotation][i][j] != 0:
                    new_tile = Tile(self.board.tile_lib[self.name],
                                    init_pos + pygame.Vector2(j * self.settings.tile_size, i * self.settings.tile_size))
                    self.tileset.add(new_tile)

    def position_tile(self, line, column, rotation):
        pos = self.board_position + pygame.Vector2(column * self.settings.tile_size,
                                                   line * self.settings.tile_size)
        self.tileset.empty()
        for i in range(len(self.data[rotation])):
            for j in range(len(self.data[rotation][i])):
                if self.data[rotation][i][j] != 0:
                    new_tile = Tile(self.board.tile_lib[self.name],
                                    pos + pygame.Vector2(j * self.settings.tile_size,
                                                         i * self.settings.tile_size))
                    self.tileset.add(new_tile)
        self.line = line
        self.column = column
        self.rotation = rotation
