from db_details import CONNECTION
import pymongo
from pymongo import MongoClient

class Database:
    def __init__(self):
        cluster = MongoClient(CONNECTION)
        db = cluster["sudoku-server"]
        self.collection = db["running_games"]

    def add_game(self, code, solved, playing, og, creator):
        post = {
            "_id": code,
            "solved_board": solved,
            "playing_board": playing,
            "og_board": og,
            "players": [creator]
                }
        self.collection.insert_one(post)

    def add_player_to_game(self, code, player):
        query = {"code": code}
        self.collection.update_one(query, {"$set": {"players": player}})


    def update_game(self, code, playing):
        query = {"code": code}
        self.collection.update_one(query, {"$set": {"playing_board": playing}})
        return self.get_game(code)

    def get_game(self, code):
        query = {"code": code}
        self.collection.find(query)


    def delete_game(self, code):
        query = {"code": code}
        self.collection.delete_one(query)

    def get_all_games(self):
        ids = self.collection.find().distinct('_id')
        return [str(id) for id in ids]


