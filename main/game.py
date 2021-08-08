import time
from sudoku_generator import SudokuBoard

class Game:
    def __init__(self):
        self.code = self.generate_code()
        self.solved_board = SudokuBoard().solve_board()
        self.game_board = SudokuBoard(self.solved_board).create_playable_board()
        self.og_board = self.game_board.copy()

    def generate_code(self):
        now = str(time.time())
        now = now.replace('.', "")
        now = now[-1:-11:-1]
        print("now",len(now))
        code = ""
        for start in range(3):
            sum = 0
            for i in range((start*3), (start*3)+3):
                sum += int(now[i])
            num = sum % 62
            if num <= 10:
                code += chr(48+(num % 10))
            elif num <= 36 and num > 10:
                code += chr(65 + (num % 26))
            elif num <= 62 and num > 36:
                code += chr(97 + (num % 26))
        code += str(int(now[-1])*int(now[1]))[-1]
        return code

    def add_to_db(self):
        pass

    def update_db(self):
        pass

    def delete_from_db(self):
        pass




Game()
