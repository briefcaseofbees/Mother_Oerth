from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uuid, logging, json

app = FastAPI()

class Server:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, player_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[player_id] = websocket

    def disconnect(self, player_id: str):
        self.active_connections.pop(player_id, None)

    async def send_to_player(self, player_id: str, message: dict):
        websocket = self.active_connections.get(player_id)
        if websocket:
            await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        for websocket in self.active_connections.values():
            await websocket.send_text(json.dumps(message))



server = Server()


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await server.connect(player_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            # route message to appropriate handler
            await handle_message(player_id, message)
    except WebSocketDisconnect:
        server.disconnect(player_id)


