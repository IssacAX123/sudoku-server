import asyncio
import websockets
import json
from main.sudoku_db import Database
from main.game import Game
from main.sudoku_generator import SudokuBoard
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
                game_to_send["extra_info"] = "CREATE_GAME"
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
                    game_to_send["extra_info"] = "JOIN_GAME"
                    print(game_to_send)
                    await websocket.send(json.dumps(game_to_send))

                    player_update_json = {"response": "NEW_PLAYER", "name": name}
                    players_to_broadcast = DB.get_players_in_game(code)
                    for player in players_to_broadcast:
                        if player != name:
                            connection = CONNECTED[player]["websocket"]
                            await connection.send(json.dumps(player_update_json))
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
                del game_to_send["og_board"]
                del game_to_send["solved_board"]
                del game_to_send["_id"]
                del game_to_send["players"]
                game_to_send["response"] = "GAME_JSON"
                game_to_send["extra_info"] = "MOVE_JSON"

                players_to_broadcast = DB.get_players_in_game(code)
                print(players_to_broadcast)
                errors = getErrors(game_to_send["playing_board"], number, location)
                errors_json = {"response": "ERRORS", "errors": errors, "changed_location": location}
                for player in players_to_broadcast:
                    connection = CONNECTED[player]["websocket"]
                    if player != name:
                        await connection.send(json.dumps(game_to_send))
                    await connection.send(json.dumps(errors_json))

    except websockets.ConnectionClosedError:
        print("connection closed")
        name = str(websocket.remote_address[0]) + "-" + str(websocket.remote_address[1])
        code = CONNECTED[name]["code"]
        DB.remove_player_in_game(code, name)
        player_update_json = {"response": "PLAYER_DISCONNECTED", "name": name}
        players_to_broadcast = DB.get_players_in_game(code)
        for player in players_to_broadcast:
            if player != name:
                connection = CONNECTED[player]["websocket"]
                await connection.send(json.dumps(player_update_json))




def getErrors(board, value, location):
    if value != 0:
        errors = []
        getRowErrors(board, value, location[0], location[1],errors)
        getColumnErrors(board, value, location[0], location[1], errors)
        getBoxErrors(board, value, location[0], location[1], errors)
        if len(errors) > 0:
            errors.append(location)
    else:
        errors = []
    return errors

def getRowErrors(board, value, row, column, errors):
    for y in range(9):
        if value == board[row][y]:
            if column != y:
                errors.append([row, y])


def getColumnErrors(board, value, row, column, errors):
    for x in range(9):
        if value == board[x][column]:
            if row != x:
                errors.append([x,column])


def getBoxErrors(board, value, row, column, errors):
    row_start = row - row % 3
    column_start = column - column % 3
    for x in range(row_start, row_start + 3):
        for y in range(column_start, column_start + 3):
            if value == board[x][y]:
                if (x,y) != (row, column):
                    errors.append([x,y])


start_server = websockets.serve(server, "localhost", 80)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
