from typing import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

class SignalingServer:
    rooms: Dict[str, List[WebSocket]]
    app: FastAPI
    
    def __init__(self, app: FastAPI):
        self.rooms = {}
        self.app = app
        self.register_routes()
    
    def register_routes(self):
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.on_connect(websocket)
            
    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                message = await websocket.receive_json()
                await self.on_message(websocket, message)
        except WebSocketDisconnect:
            await self.on_disconnect(websocket)
    
    async def on_message(self, websocket: WebSocket, message: dict):
        action = message.get("action")
        room = message.get("room")
        data = message.get("data")
        
        if action == "join":
            await self.join_room(websocket, room)
        elif action == "data":
            await self.broadcast(room, {"type": "data", "data": data}, exclude_websocket = websocket)
        elif action == "leave":
            await self.leave_room(websocket, room)
        
    async def join_room(self, websocket: WebSocket, room: str):
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(websocket)
        await self.broadcast(room, {"type": "join", "message": "A user has joined the room."}, exclude_websocket = websocket)
        
    async def leave_room(self, websocket: WebSocket, room: str):
        if room in self.rooms and websocket in self.rooms[room]:
            self.rooms[room].remove(websocket)
            if not self.rooms[room]:
                del self.rooms[room]
            await self.broadcast(room, {"type": "leave", "message": "A user has left the room"})
        
    async def broadcast(self, room: str, message: dict, exclude_websocket: WebSocket = None):
        if room in self.rooms:
            for ws in self.rooms[room]:
                if ws != exclude_websocket:
                    await ws.send_json(message)
    
    async def on_disconnect(self, websocket: WebSocket):
        for room, connections in list(self.rooms.items()):
            if websocket in connections:
                await self.leave_room(websocket, room)
        