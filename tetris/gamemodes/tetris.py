from .gamemode import GameMode
import pygame
from ..tiles import Board, Tetromino, Tile
from ..rl import ListMoves
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
        self.moves = []

        self.debug_autoplay = settings.DEBUG_AUTOMOVE
        self.autoplay_timer = 0
        self.autoplay_counter = 0
        self.autoplay_move = 0
        self.autoplaying = False

        self.generate_tetromino()
        self.evaluate_next_pieces()

        self.back_to_back = False
        self.combo = -1

        self.training_mode = settings.TRAINING_MODE

    def loop(self, events):
        for event in events:
            if event.type == pygame.USEREVENT+1:
                self.tile_placed(event.tileList, event.tileName,
                                 event.tilePos, event.tileRotation,
                                 event.lastMovement, event.lastWallkick)
            if event.type == pygame.KEYDOWN:
                if not self.training_mode:
                    if event.key == pygame.K_LSHIFT:
                        self.hold()
                    elif event.key == pygame.K_a:
                        self.current_tetromino.press_side(-1, 0, 'Left')
                    elif event.key == pygame.K_d:
                        self.current_tetromino.press_side(+1, 0, 'Right')
                    elif event.key == pygame.K_s:
                        self.current_tetromino.press_side(0, +1, 'Down')
                    elif event.key == pygame.K_k:
                        self.current_tetromino.rotate(-1, 'Rotate CClockwise')
                    elif event.key == pygame.K_l:
                        self.current_tetromino.rotate(+1, 'Rotate Clockwise')
                    elif event.key == pygame.K_SPACE:
                        self.current_tetromino.lock_piece()
                else:
                    if event.key == pygame.K_LSHIFT:
                        self.hold()
                    elif event.key == pygame.K_a:
                        self.autoplay_move = (self.autoplay_move - 1) % len(self.moves)
                    elif event.key == pygame.K_d:
                        self.autoplay_move = (self.autoplay_move + 1) % len(self.moves)
                    elif event.key == pygame.K_SPACE:
                        new_line, new_column, new_rotation = self.moves[self.autoplay_move][-1]
                        self.autoplay_move = 0
                        self.current_tetromino.position_tile(new_line, new_column, new_rotation)
                        self.current_tetromino.lock_piece()

        self.screen.fill(0)
        self.board.update()
        self.current_tetromino.update(events)
        self.next_pieces.draw(self.screen)
        self.hold_piece.draw(self.screen)
        if self.debug_autoplay or self.training_mode:
            #print(self.moves[self.autoplay_move][-1])
            self.current_tetromino.debug_shadow_line = self.moves[self.autoplay_move][-1][0]
            self.current_tetromino.debug_shadow_column = self.moves[self.autoplay_move][-1][1]
            self.current_tetromino.debug_shadow_rotation = self.moves[self.autoplay_move][-1][2]
            self.current_tetromino.calculate_shadow()
            if self.debug_autoplay:
                self.handle_debug(events)

    def handle_debug(self, events):
        pressed_x = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.current_tetromino.line = 19
                    self.current_tetromino.column = 4
                    self.current_tetromino.rotation = 0
                    self.current_tetromino.restart_tile()
                    self.autoplay_counter = 0
                    self.autoplay_timer = 0
                    self.autoplay_move += 1
                    self.autoplaying = 1
                    if self.autoplay_move == len(self.moves):
                        self.autoplay_move = 0
                    print('Autoplay')
                    print(f'{self.moves[self.autoplay_move][-1]}')
                if event.key == pygame.K_x:
                    pressed_x = True
        if self.autoplaying:
            if pressed_x:
                name_to_key = {
                    'S': pygame.K_s,
                    'A': pygame.K_a,
                    'D': pygame.K_d,
                    'L': pygame.K_l,
                    'K': pygame.K_k
                }
                print(f'Command: {self.moves[self.autoplay_move][self.autoplay_counter]}')
                pygame.event.post(
                    pygame.event.Event(pygame.KEYDOWN,
                                       key=name_to_key[self.moves[self.autoplay_move][self.autoplay_counter]]))
                self.autoplay_counter += 1
                self.autoplay_timer = 0

                if self.autoplay_counter == len(self.moves[self.autoplay_move]) - 1:
                    self.autoplay_counter = 0
                    self.autoplaying = 0
            else:
                self.autoplay_timer += 1

    def tile_placed(self, tile_list, tile_name, tile_position, tile_rotation, last_movement, last_wallkick):
        for tile in tile_list:
            self.board.change(tile, tile_name)
        cleared_lines, pc, tspin = \
            self.board.clear_lines(tile_name, tile_position, tile_rotation, last_movement, last_wallkick)
        self.generate_tetromino()
        self.evaluate_next_pieces()
        self.has_held = False
        if cleared_lines > 0:
            self.combo += 1
            if cleared_lines == 4 or tspin:
                if self.back_to_back:
                    print('Back to Back')
                self.back_to_back = True
            else:
                self.back_to_back = False
            print(f'Lines Cleared: {cleared_lines}, combo: {self.combo}')
            if tspin:
                print('Tspin')
            if pc:
                print('Perfect Clear')
        else:
            self.combo = -1

    def generate_tetromino(self):
        if self.current_bag_index == 7:
            self.current_bag = self.next_bag.copy()
            random.shuffle(self.next_bag)
            self.current_bag_index = 0
        self.current_tetromino = Tetromino(self.board, self.current_bag[self.current_bag_index],
                                           self.board_position, self.settings, self.screen)
        self.current_bag_index += 1
        self.moves = ListMoves(self.board, self.current_tetromino.name).list_moves()
        #print(self.moves)
        #print(f'Found {len(self.moves)} moves')

    def evaluate_next_pieces(self):
        self.next_pieces.empty()
        all_pieces = self.current_bag+self.next_bag
        #print(all_pieces)
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
                self.evaluate_next_pieces()
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
            self.autoplay_counter = 0
            self.autoplay_move = 0
            self.moves = ListMoves(self.board, self.current_tetromino.name).list_moves()
