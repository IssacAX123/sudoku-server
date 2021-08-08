import time
from sudoku_generator import SudokuBoard

class Game:
    def __init__(self, db, creator):
        self.db = db
        self.code = self.generate_code()
        self.solved_board = SudokuBoard().solve_board()
        self.playing_board = SudokuBoard(self.solved_board).create_playable_board()
        self.players = [creator]
        self.og_board = self.playing_board.copy()


    def generate_code(self):
        finished  = False
        code = ""
        while not finished:
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
            if code not in self.get_all_games():
                finished = True
        return code

    def add_to_db(self):
        self.db.add_game(self.code, self.solved_board, self.playing_board, self.og_board, self.players[0])

    def update_player_in_db(self):
        if not self.players:
            self.delete_from_db()
        else:
            self.db.update_player_in_db(self.code, self.solved_board, self.playing_board, self.og_board)

    def update_db(self, location, number):
        self.db.update_game(self.code, location, number)

    def delete_from_db(self):
        self.db.delete_game(self.code)

    def get_all_games(self):
        return self.db.get_all_games()




Game()
