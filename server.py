import asyncio
import websockets
import json
from main.sudoku_db import Database
from main.game import Game
PORT = 5556
CONNECTED = {}
DB = Database()


async def server(websocket, path):
    print("conn")
    name = str(websocket.remote_address[0]) + "-" + str(websocket.remote_address[1])
    CONNECTED[name] = {"websocket": websocket}
    init_json = {"name": name}
    await websocket.send(json.dumps(init_json))
    try:
        async for message in websocket:
            json.load(message)
            if message["event"] == "create_game":
                name = message["name"]
                game = Game(DB, CONNECTED[name])
                code = game.get_code()
                CONNECTED[name]["code"] = code
                game_to_send = DB.get_game(code)
                await websocket.send(json.dumps(game_to_send))
            if message["event"] == "join_game":
                name = message["name"]
                code = message["code"]
                CONNECTED[name]["code"] = code
                DB.add_player_in_game(code, name)
                game_to_send = DB.get_game(code)
                await websocket.send(json.dumps(game_to_send))
            if message["event"] == "move":
                name = message["name"]
                code = message["code"]
                location = message["location"]
                number = message["number"]
                DB.update_game(code, location, number)
                game_to_send = DB.get_game(code)
                players_to_broadcast = DB.get_players_in_game(code)
                async for player in players_to_broadcast:
                    connection = CONNECTED[player]["websocket"]
                    await connection.send(json.dumps(game_to_send))
    except:
        name = str(websocket.remote_address[0]) + "-" + str(websocket.remote_address[1])
        code = CONNECTED[name]["code"]
        DB.remove_player_in_game(code, name)


start_server = websockets.serve(server, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()