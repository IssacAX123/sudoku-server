from main.db_details import CONNECTION
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

    def add_player_in_game(self, code, player):
        query = {"_id": code}
        self.collection.update_one(query, {"$push": {"players": player}})

    def remove_player_in_game(self, code, player):
        query = {"_id": code}
        self.collection.update_one(query, {"$pull": {"players": player}})
        length = len(self.collection.find(query)["players"])
        if length == 0:
            self.delete_game(code)

    def update_game(self, code, location, number):
        query = {"_id": code}
        index = f"playing_board.{location[0]}.{location[1]}"
        self.collection.update_one(query, {"$set": {index: number}})
        return self.get_game(code)

    def get_game(self, code):
        query = {"_id": code}
        self.collection.find(query)

    def delete_game(self, code):
        query = {"_id": code}
        self.collection.delete_one(query)

    def get_all_games(self):
        ids = self.collection.find().distinct('_id')
        return [str(id) for id in ids]

    def get_players_in_game(self, code):
        query = {"_id": code}
        return self.collection.find(query)["players"]



