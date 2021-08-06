from random import randint


class SudokuBoard:
    def __init__(self):
        self.board = [[0 for y in range(9)] for x in range(9)]
        self.initial_fill()

    def initial_fill(self, fill_number=9):
        filled = set()
        for i in range(fill_number):
            in_filled = False
            while not in_filled:
                x_coord = randint(0, 8)
                y_coord = randint(0, 8)
                if (x_coord, y_coord) not in filled:
                    value = randint(1, 9)
                    if not self.checkRow(value, x_coord) and not self.checkColumn(value, y_coord) and \
                        not self.checkBox(value, x_coord,y_coord):
                        self.board[x_coord][y_coord] = value
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

    def checkRow(self, value, row):
        for y in range(9):
            if value == self.board[row][y]:
                return True
        return False

    def checkColumn(self, value, column):
        for x in range(9):
            if value == self.board[x][column]:
                return True
        return False

    def checkBox(self, value, row, column):
        row_start = row - row % 3
        column_start = column - column % 3
        for x in range(row_start, row_start+3):
            for y in range(column_start, column_start+3):
                if value == self.board[x][y]:
                    return True
        return False

    def solve_board(self):
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    for value in range(1, 10):
                        if not self.checkRow(value, row) and not self.checkColumn(value, column) and \
                                not self.checkBox(value, row, column):
                            self.board[row][column] = value
                            if self.solve_board():
                                return True
                            else:
                                self.board[row][column] = 0
                    return False
        return True


sb = SudokuBoard()
sb.print()
print("*******************************************")
sb.solve_board()
sb.print()
