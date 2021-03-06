from random import randint
import copy


class SudokuBoard:
    def __init__(self, user_board=None):
        if user_board is None:
            self.board = [[0 for y in range(9)] for x in range(9)]
            self.initial_fill()
        if user_board is not None:
            self.board = user_board


    def initial_fill(self, fill_number=8):
        filled = set()
        x_coord = 0
        y_coord = randint(6, 8)
        value = randint(1, 9)
        self.board[x_coord][y_coord] = value
        filled.add((x_coord, y_coord))
        for i in range(fill_number//2):
            in_filled = False
            while not in_filled:
                x_coord = i
                y_coord = i
                if (x_coord, y_coord) not in filled:
                    value = randint(1, 9)
                    if not self.checkRow(self.board, value, x_coord) and not self.checkColumn(self.board, value, y_coord) and \
                            not self.checkBox(self.board, value, x_coord, y_coord):
                        self.board[x_coord][y_coord] = value
                        filled.add((x_coord, y_coord))
                        in_filled = True

        for i in range(fill_number//2):
            in_filled = False
            while not in_filled:
                x_coord = randint(0, 8)
                y_coord = randint(0, 8)
                if (x_coord, y_coord) not in filled:
                    value = randint(1, 9)
                    if not self.checkRow(self.board, value, x_coord) and not self.checkColumn(self.board, value,
                                                                                              y_coord) and \
                            not self.checkBox(self.board, value, x_coord, y_coord):
                        self.board[x_coord][y_coord] = value
                        filled.add((x_coord, y_coord))
                        in_filled = True


    def print(self):
        print('  1 2 3   4 5 6   7 8 9')
        for row_index, row in enumerate(self.board):
            for column_index, column in enumerate(row):
                if (column_index + 1) % 9 != 0:
                    if (column_index + 1) != 9 and (column_index + 1) % 3 == 0:
                        print(column, end=" | ")
                    else:
                        if (column_index + 1) % 9 == 1:
                            print(row_index + 1, end="|")
                            print(column, end=" ")
                        else:
                            print(column, end=" ")
                else:
                    print(column, end="\n")
                    if (row_index + 1) % 3 == 0:
                        print(' ', '-' * 21)

    @staticmethod
    def checkRow(board, value, row):
        for y in range(9):
            if value == board[row][y]:
                return True
        return False

    @staticmethod
    def checkColumn(board, value, column):
        for x in range(9):
            if value == board[x][column]:
                return True
        return False

    @staticmethod
    def checkBox(board, value, row, column):
        row_start = row - row % 3
        column_start = column - column % 3
        for x in range(row_start, row_start + 3):
            for y in range(column_start, column_start + 3):
                if value == board[x][y]:
                    return True
        return False

    def solve_board(self):
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    for value in range(1, 10):
                        if not self.checkRow(self.board, value, row) and not self.checkColumn(self.board, value, column) and \
                                not self.checkBox(self.board, value, row, column):
                            self.board[row][column] = value
                            if self.solve_board():
                                return True
                            else:
                                self.board[row][column] = 0
                    return False
        return True

    def create_playable_board(self):
        play_board = copy.deepcopy(self.board)
        filled = [(randint(0,8), randint(0, 8)) for x in range(81- randint(30, 40))]
        for coord in filled:
            play_board[coord[0]][coord[1]] = 0
        return play_board

    def get_board(self):
        return self.board

    def encode(self):
        return self.board



