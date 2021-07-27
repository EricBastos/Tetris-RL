import numpy as np
from bitarray import bitarray
from bitarray.util import ba2int as ba2int

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
        self.hold_tetromino = 'E'
        self.has_held = False
        self.lines_cleared = 0

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

        self.frames = 0

    def loop(self, events):
        for event in events:
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
                        fb = self.current_tetromino.lock_piece()
                        self.tile_placed(fb[0], fb[1], fb[2], fb[3], fb[4], fb[5])
                        return
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
                        fb = self.current_tetromino.lock_piece()
                        self.tile_placed(fb[0], fb[1], fb[2], fb[3], fb[4], fb[5])
                if event.key == pygame.K_g:
                    self.reset()
                    return
                if event.key == pygame.K_v:
                    state, reward, done, moves = self.step(random.sample(self.moves, 1)[0][-1])
                    #print(random.sample(self.moves, 1)[0][-1])
                    #print(state.type)
                    #print(state.shape)

        self.screen.fill(0)
        self.board.update()
        self.current_tetromino.update(events)
        self.next_pieces.draw(self.screen)
        self.hold_piece.draw(self.screen)
        if self.debug_autoplay:
            # print(self.moves[self.autoplay_move][-1])
            self.current_tetromino.debug_shadow_line = self.moves[self.autoplay_move][-1][0]
            self.current_tetromino.debug_shadow_column = self.moves[self.autoplay_move][-1][1]
            self.current_tetromino.debug_shadow_rotation = self.moves[self.autoplay_move][-1][2]
            self.current_tetromino.calculate_shadow()
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
                    #print('Autoplay')
                    #print(f'{self.moves[self.autoplay_move][-1]}')
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
                #print(f'Command: {self.moves[self.autoplay_move][self.autoplay_counter]}')
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
        garbage_sent = 0
        for tile in tile_list:
            self.board.change(tile, tile_name)
        cleared_lines, pc, tspin = \
            self.board.clear_lines(tile_name, tile_position, tile_rotation, last_movement, last_wallkick)
        #print(f'{cleared_lines}, {pc}, {tspin}')
        if self.board.matrix[21][1] != 'E' or \
                self.board.matrix[21][2] != 'E' or \
                self.board.matrix[21][3] != 'E' or \
                self.board.matrix[21][4] != 'E' or \
                self.board.matrix[21][5] != 'E' or \
                self.board.matrix[21][6] != 'E' or \
                self.board.matrix[21][7] != 'E' or \
                self.board.matrix[21][8] != 'E' or \
                self.board.matrix[21][9] != 'E' or \
                self.board.matrix[21][10] != 'E':
            return 0, True

        self.generate_tetromino()
        self.evaluate_next_pieces()
        self.has_held = False
        back_to_back = False
        if cleared_lines > 0:
            self.combo += 1
            if cleared_lines == 4 or tspin:
                if self.back_to_back:
                    back_to_back = True
                    garbage_sent += 1
                self.back_to_back = True
            else:
                self.back_to_back = False
            # print(f'Lines Cleared: {cleared_lines}, combo: {self.combo}')
            if 2 <= self.combo <= 3:
                garbage_sent += 1
            elif 4 <= self.combo <= 5:
                garbage_sent += 2
            elif 6 <= self.combo <= 7:
                garbage_sent += 3
            elif 8 <= self.combo <= 10:
                garbage_sent += 4
            elif self.combo > 10:
                garbage_sent += 5

            if tspin:
                garbage_sent += 2 * cleared_lines
            else:
                if cleared_lines == 4:
                    garbage_sent += 4
                else:
                    garbage_sent += cleared_lines - 1
            if pc:
                garbage_sent = 10
        else:
            self.combo = -1
        return self.reward_engineering(cleared_lines, pc, tspin, self.combo, back_to_back), False

    def reward_engineering(self, cleared_lines, pc, tspin, combo, back_to_back):
        reward = 0
        if back_to_back:
            print('back to back')
            reward += 10

        if 2 <= combo <= 3:
            print(f'combo {combo}')
            reward += 1
        elif 4 <= combo <= 5:
            print(f'combo {combo}')
            reward += 3
        elif 6 <= combo <= 7:
            print(f'combo {combo}')
            reward += 6
        elif 8 <= combo <= 10:
            print(f'combo {combo}')
            reward += 10
        elif combo > 10:
            print(f'combo {combo}')
            reward += 15

        if tspin:
            print(f'tspin {cleared_lines}')
            reward += 7.5 * cleared_lines ** 2
        else:
            if cleared_lines == 4:
                reward += 20
            else:
                reward += cleared_lines ** 2
            if cleared_lines:
                self.lines_cleared += cleared_lines
                print(f'cleared {cleared_lines}')
        if pc:
            print('pc')
            reward += 100
        reward += 5*self.lines_cleared
        column_height = self.get_stack_height_info()
        reward -= 0.3 * np.sum(column_height)
        for i in range(9):
            reward -= 0.1 * np.abs(column_height[i]-column_height[i+1])
        return reward

    def get_stack_height_info(self):
        column_height = np.zeros(10)
        for j in range(1, 11):
            for i in range(20, 40):
                if self.board.matrix[i][j] != 'E':
                    column_height[j - 1] = 40-i
                    break
        return column_height

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
        # print(f'Found {len(self.moves)} moves')

    def evaluate_next_pieces(self):
        self.next_pieces.empty()
        all_pieces = self.current_bag + self.next_bag
        # print(all_pieces)
        draw_position = pygame.Vector2(self.settings.screen_width / 2 + 8 * self.settings.tile_size,
                                       1 * self.settings.tile_size)
        for i in range(self.current_bag_index, self.current_bag_index + 5):
            tile_name = all_pieces[i]
            data = Tetromino.tetromino_lib[tile_name][0]
            xoffset = 0
            if tile_name == 'I' or tile_name == 'O':
                xoffset = -self.settings.tile_size / 2
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if data[i][j] != 0:
                        new_tile = Tile(self.board.tile_lib[tile_name],
                                        draw_position + pygame.Vector2(j * self.settings.tile_size + xoffset,
                                                                       i * self.settings.tile_size))
                        self.next_pieces.add(new_tile)
            draw_position += pygame.Vector2(0, 3 * self.settings.tile_size)

    def hold(self):
        if not self.has_held:
            self.has_held = True
            self.current_tetromino.kill()
            if self.hold_tetromino == 'E':
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

    def reset(self, type):
        self.autoplay_timer = 0
        self.autoplay_counter = 0
        self.autoplay_move = 0
        self.autoplaying = False
        self.lines_cleared = 0
        self.board.board.empty()
        self.board = Board(self.board_position, self.settings, self.screen)

        self.next_pieces.empty()
        self.hold_piece.empty()
        self.hold_tetromino = 'E'
        self.has_held = False

        self.current_tetromino = None
        self.current_bag_index = 0
        self.current_bag = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        self.next_bag = self.current_bag
        random.shuffle(self.current_bag)
        random.shuffle(self.next_bag)

        self.generate_tetromino()
        self.evaluate_next_pieces()

        self.back_to_back = False
        self.combo = -1

        self.frames = 0

        return self.extract_state(type)

    def extract_state(self, type):
        if type == 'dqn':
            state, moves = self.extract_state_dqn()
        elif type == 'ppo':
            state = self.extract_ppo_state()
            moves = []
        else:
            state = []
            moves = []
        return state, moves

    def step(self, action, type):
        self.frames += 1
        if action[2] != 4:
            new_line, new_column, new_rotation = action
            self.current_tetromino.position_tile(new_line, new_column, new_rotation)
            fb = self.current_tetromino.lock_piece()
            reward, done = self.tile_placed(fb[0], fb[1], fb[2], fb[3], fb[4], fb[5])
        else:
            self.hold()
            reward, done = self.reward_engineering(0, False, False, 0, False), False

        state, moves = self.extract_state(type)

        if len(self.moves) == 0:
            done = True

        if done:
            reward = -4500 * np.exp(-self.frames / 25)

        return state, reward, done, moves

    def extract_state_dqn(self):
        slice_matrix = self.board.matrix[20:40, 1:11]
        line_matrix = np.array(list(map(ord, np.hstack(slice_matrix))))
        all_pieces = self.current_bag + self.next_bag
        next_pieces_name = all_pieces[self.current_bag_index : self.current_bag_index+5]

        moves = []

        for move in self.moves:
            moves.append(move[-1])
        if not self.has_held:
            moves.append((0, 0, 4))

        state_bits = bitarray('0' * 3)
        next_pieces_bits = []
        for next_piece in next_pieces_name:
            next_pieces_bits += Tetromino.tetromino_encoding[next_piece]
        bit_data = Tetromino.tetromino_encoding[self.current_tetromino.name] + \
                          next_pieces_bits + \
                          Tetromino.tetromino_encoding[self.hold_tetromino]
        bit_data = np.concatenate((bit_data, line_matrix != 69))
        state_bits.extend(bit_data)
        state_data = np.packbits(bit_data).astype(np.float32)
        #print(len(moves))
        return state_data, moves

    def extract_ppo_state(self):
        slice_matrix = self.board.matrix[20:40, 1:11]
        line_matrix = np.array(list(map(ord, np.hstack(slice_matrix))))
        line_matrix = line_matrix != 69
        line_matrix = line_matrix.astype(np.float32)
        state_matrix = line_matrix.reshape((20, 10, 1))

        all_pieces = self.current_bag + self.next_bag
        next_pieces_name = all_pieces[self.current_bag_index: self.current_bag_index + 5]

        action_mask = np.ones((4, 20, 11))
        #pos_only = []
        for move in self.moves:
            line, column, rotation = move[-1]
            if line >= 20:
                #pos_only.append(move[-1])
                column += 1
                line -= 20
                action_mask[rotation, line, column] = 0
        #print(pos_only)
        action_mask = action_mask.reshape((-1))
        action_mask = np.append(action_mask, self.has_held)
        pieces = [self.current_tetromino.name] + next_pieces_name + [self.hold_tetromino]
        pieces = np.array(list(map(ord, pieces)))
        state_info = [state_matrix, pieces, action_mask]

        return state_info