from ..tiles import Tetromino, Board


class ListMoves:

    def __init__(self, board: Board, name: str):
        self.board = board
        self.name = name
        self.data = Tetromino.tetromino_lib[self.name]

    def list_moves(self):
        moves = []
        for rotation in range(4):
            for column in range(-1, 11):
                consecutive = 0
                for line in reversed(range(40)):
                    if not self.check_collision(line, column, rotation):
                        if consecutive > 0:
                            break
                        else:
                            consecutive = 1
                            print(f'Maybe {line} {column} {rotation}')
                            move = []
                            if not self.check_collision(line-1, column, rotation):
                                self.treeRecursion(line-1, column, rotation, 'down', move, 0)
                            if len(move) == 0 and not self.check_collision(line, column-1, rotation):
                                self.treeRecursion(line, column-1, rotation, 'right', move, 0)
                            if len(move) == 0 and not self.check_collision(line, column+1, rotation):
                                self.treeRecursion(line, column+1, rotation, 'left', move, 0)
                            if len(move) == 0:
                                fine, new_column, new_line, new_rotation = self.check_rotation(line, column, rotation, 'clockwise')
                                if fine:
                                    self.treeRecursion(new_line, new_column, new_rotation, 'cclockwise', move, 0)
                            if len(move) == 0:
                                fine, new_column, new_line, new_rotation = self.check_rotation(line, column, rotation, 'cclockwise')
                                if fine:
                                    self.treeRecursion(new_line, new_column, new_rotation, 'clockwise', move, 0, (line==36 and column ==2 and rotation == 3))
                            if len(move) > 0:
                                move.append((line, column, rotation))
                                moves.append(move)
                                print(f'Found {line} {column} {rotation}')
                            else:
                                print(f'No luck {line} {column} {rotation}')

                    else:
                        consecutive = 0
        return moves

    def treeRecursion(self, line, column, rotation, last_dir, move, same_height, debug = False) -> bool:
        if line == 19 and column == 4 and rotation == 0:
            move.append(last_dir)
            return True
        if line < 19:
            return False
        if same_height == 5:
            return False
        if not self.check_collision(line - 1, column, rotation):
            found = self.treeRecursion(line - 1, column, rotation, 'down', move, 0, debug)
            if found:
                move.append(last_dir)
                return True
        if len(move) == 0 and not self.check_collision(line, column - 1, rotation) and last_dir != 'left':
            found = self.treeRecursion(line, column - 1, rotation, 'right', move, same_height+1, debug)
            if found:
                move.append(last_dir)
                return True
        if len(move) == 0 and not self.check_collision(line, column + 1, rotation) and last_dir != 'right':
            found = self.treeRecursion(line, column + 1, rotation, 'left', move, same_height+1, debug)
            if found:
                move.append(last_dir)
                return True
        if len(move) == 0:
            fine, new_column, new_line, new_rotation = self.check_rotation(line, column, rotation, 'clockwise')
            if fine and last_dir != 'clockwise' and new_line <= line:
                htemp = 0
                if new_line == line:
                    htemp = same_height+1
                found = self.treeRecursion(new_line, new_column, new_rotation, 'cclockwise', move, htemp, debug)
                if found:
                    move.append(last_dir)
                    return True
        if len(move) == 0:
            fine, new_column, new_line, new_rotation = self.check_rotation(line, column, rotation, 'cclockwise')
            if fine and last_dir != 'cclockwise' and new_line <= line:
                htemp = 0
                if new_line == line:
                    htemp = same_height+1
                found = self.treeRecursion(new_line, new_column, new_rotation, 'clockwise', move, htemp, debug)
                if found:
                    move.append(last_dir)
                    return True
        return False

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
