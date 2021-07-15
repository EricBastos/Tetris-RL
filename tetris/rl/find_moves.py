from ..tiles import Tetromino, Board
import numpy as np
import queue


class ListMoves:

    def __init__(self, board: Board, name: str):
        self.board = board
        self.name = name
        self.data = Tetromino.tetromino_lib[self.name]
        self.moves_table = np.full((40, 12, 4), 'O', dtype=str)
        self.count_table = np.full((40, 12, 4), 100, dtype=int)
        self.table_queue = queue.SimpleQueue()
        self.board_dict = {}
        self.position_dict = {}
        self.moves = []

    def list_moves(self):
        init_pos = [19, 4, 0, []]

        for rotation in range(4):
            for column in range(-1, 11):
                for line in reversed(range(40)):
                    if not self.check_collision(line, column, rotation) and \
                            self.check_collision(line+1, column, rotation):
                        self.position_dict[f'({line}, {column}, {rotation})'] = True

        self.moves_table[init_pos[0], init_pos[1]+1, init_pos[2]] = 'I'
        self.count_table[init_pos[0], init_pos[1]+1, init_pos[2]] = 0
        self.add_actions(init_pos)

        self.tableBFS()

        return self.moves

    def tableBFS(self):
        while not self.table_queue.empty():
            action = self.table_queue.get()
            line = action[0]
            column = action[1]
            rotation = action[2]
            command = action[3]
            command_list = action[4]
            position_key = f'({line}, {column}, {rotation})'
            board_key = 1
            if position_key in self.position_dict:
                for i in range(len(self.data[rotation])):
                    for j in range(len(self.data[rotation][i])):
                        if self.data[rotation][i][j] != 0:
                            board_key = board_key * 10000 + (i + line) * 100 + (j + column)
                if board_key not in self.board_dict:
                    self.board_dict[board_key] = True
                    command_list.pop()
                    self.moves.append(command_list+[(line, column, rotation)])

            if command == 'A':
                if not self.check_collision(line, column - 1, rotation):
                    if self.count_table[line, column + 1, rotation] + 1 < self.count_table[line, column - 1 + 1, rotation]:
                        self.count_table[line, column - 1 + 1, rotation] = self.count_table[line, column + 1, rotation] + 1
                        self.moves_table[line, column - 1 + 1, rotation] = command
                        # Adicionar ações
                        new_pos = [line, column - 1, rotation, command_list]
                        self.add_actions(new_pos)

            elif command == 'S':
                if not self.check_collision(line + 1, column, rotation):
                    if self.count_table[line, column + 1, rotation] + 1 < self.count_table[line + 1, column + 1, rotation]:
                        self.count_table[line + 1, column + 1, rotation] = self.count_table[line, column + 1, rotation] + 1
                        self.moves_table[line + 1, column + 1, rotation] = command
                        # Adicionar ações
                        new_pos = [line + 1, column, rotation, command_list]
                        self.add_actions(new_pos)

            elif command == 'D':
                if not self.check_collision(line, column + 1, rotation):
                    if self.count_table[line, column + 1, rotation] + 1 < self.count_table[line, column + 1 + 1, rotation]:
                        self.count_table[line, column + 1 + 1, rotation] = self.count_table[line, column + 1, rotation] + 1
                        self.moves_table[line, column + 1 + 1, rotation] = command
                        # Adicionar ações
                        new_pos = [line, column + 1, rotation, command_list]
                        self.add_actions(new_pos)

            elif command == 'L':
                fine, new_column, new_line, new_rotation = self.check_rotation(line, column, rotation, 'clockwise')
                if fine:
                    if self.count_table[line, column + 1, rotation] + 1 < self.count_table[new_line, new_column + 1, new_rotation]:
                        self.count_table[new_line, new_column + 1, new_rotation] = self.count_table[line, column + 1, rotation] + 1
                        self.moves_table[new_line, new_column + 1, new_rotation] = command
                        # Adicionar ações
                        new_pos = [new_line, new_column, new_rotation, command_list]
                        self.add_actions(new_pos)

            elif command == 'K':
                fine, new_column, new_line, new_rotation = self.check_rotation(line, column, rotation, 'cclockwise')
                if fine:
                    if self.count_table[line, column + 1, rotation] + 1 < self.count_table[new_line, new_column + 1, new_rotation]:
                        self.count_table[new_line, new_column + 1, new_rotation] = self.count_table[line, column + 1, rotation] + 1
                        self.moves_table[new_line, new_column + 1, new_rotation] = command
                        # Adicionar ações
                        new_pos = [new_line, new_column, new_rotation, command_list]
                        self.add_actions(new_pos)

    def add_actions(self, info):

        self.table_queue.put([info[0], info[1], info[2], 'A', info[3]+['A']])
        self.table_queue.put([info[0], info[1], info[2], 'S', info[3]+['S']])
        self.table_queue.put([info[0], info[1], info[2], 'D', info[3]+['D']])
        self.table_queue.put([info[0], info[1], info[2], 'L', info[3]+['L']])
        self.table_queue.put([info[0], info[1], info[2], 'K', info[3]+['K']])

    def check_collision(self, line, column, rotation):
        for i in range(len(self.data[rotation])):
            for j in range(len(self.data[rotation][i])):
                if self.data[rotation][i][j] != 0:
                    try:
                        if self.board.matrix[line + i, column + j] != 'E':
                            return True
                    except (IndexError, ValueError):
                        return True
        return False

    def check_rotation(self, line, column, rotation, direction):
        if direction == 'clockwise':
            temp_rotation = (rotation + 1) % 4
        else:
            temp_rotation = (rotation - 1) % 4
        rotation_key = rotation * 10 + temp_rotation
        piece_key = 'others'
        if self.name == 'I':
            piece_key = 'I'
        detected_collision = True
        successful_test = None
        for i in range(5):
            translation = Tetromino.wall_kick[piece_key][rotation_key][i]
            if not self.check_collision(line + translation[1], column + translation[0], temp_rotation):
                successful_test = i
                detected_collision = False
                break
        if not detected_collision:
            new_column = column + Tetromino.wall_kick[piece_key][rotation_key][successful_test][0]
            new_line = line + Tetromino.wall_kick[piece_key][rotation_key][successful_test][1]
            new_rotation = temp_rotation
            return [True, new_column, new_line, new_rotation]
        return [False, 0, 0, 0]
