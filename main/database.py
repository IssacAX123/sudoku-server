from db_details import CONNECTION
import pymongo
from pymongo import MongoClient

class Database:
    def __init__(self):
        cluster = MongoClient(CONNECTION)
        db = cluster["sudoku-server"]
        self.collection = db["running_games"]

    def add_game(self, code, solved, playing, og):
        pass

    def update_game(self, code, playing):
        pass

    def delete_game(self, code):
        pass
