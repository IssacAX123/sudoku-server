import asyncio
import websockets
import json
from main.sudoku_db import Database
from main.game import Game
CONNECTED = {}
DB = Database()


async def server(websocket, path):
    print("connected")
    name = str(websocket.remote_address[0]) + "-" + str(websocket.remote_address[1])
    print("name: " + name)
    CONNECTED[name] = {"websocket": websocket}
    init_json = {"response": "INNIT", "name": name}
    await websocket.send(json.dumps(init_json))
    try:
        async for message in websocket:
            message_json = json.loads(message)
            print(message_json)
            if message_json["event"] == "create_game":
                name = message_json["name"]
                game = Game(DB, name)
                code = game.get_code()
                CONNECTED[name]["code"] = code
                game_to_send = DB.get_game(code)
                game_to_send["response"] = "GAME_JSON"
                print(game_to_send)
                await websocket.send(json.dumps(game_to_send))
            if message_json["event"] == "join_game":
                name = message_json["name"]
                code = message_json["code"]
                CONNECTED[name]["code"] = code
                if code in DB.get_all_games():
                    DB.add_player_in_game(code, name)
                    game_to_send = DB.get_game(code)
                    game_to_send["response"] = "GAME_JSON"
                    print(game_to_send)
                    await websocket.send(json.dumps(game_to_send))
                else:
                    error = {"response": "INVALID_GAME_CODE"}
                    print(error)
                    await websocket.send(json.dumps(error))
            if message_json["event"] == "move":
                name = message_json["name"]
                code = message_json["code"]
                location = message_json["location"]
                number = message_json["value"]
                DB.update_game(code, location, number)
                game_to_send = DB.get_game(code)
                game_to_send["response"] = "GAME_JSON"
                print(game_to_send)
                players_to_broadcast = DB.get_players_in_game(code)
                print(players_to_broadcast)
                for player in players_to_broadcast:
                    if player != name:
                        connection = CONNECTED[player]["websocket"]
                        await connection.send(json.dumps(game_to_send))
    except websockets.ConnectionClosedError:
        try:
            print("connection closed")
            name = str(websocket.remote_address[0]) + "-" + str(websocket.remote_address[1])
            code = CONNECTED[name]["code"]
            DB.remove_player_in_game(code, name)
        except:
            pass



start_server = websockets.serve(server, "localhost", 80)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
