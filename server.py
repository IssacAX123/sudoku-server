import asyncio
import websockets
PORT = 5556
CONNECTED = set()
async def server(websocket, path):
    print("a client connected")
    CONNECTED.add(websocket)
    try:
        async for message in websocket:
            print("received message from client:", message)
            for conn in CONNECTED:
                if conn != websocket:
                    await conn.send("recieved message: " + message)
    except:
        pass

start_server = websockets.serve(server, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()