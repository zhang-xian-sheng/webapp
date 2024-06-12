#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
import uvicorn
import traceback
import websockets
from typing import List, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.usernames: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, user_name: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.usernames[websocket] = user_name
        await self.broadcast(f"{user_name} joined the chat", user_name)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        username = self.usernames.pop(websocket, "Unknown user")
        return username

    async def broadcast(self, message: str, user_name=None):
        for connection in self.active_connections:
            current_user_name = self.usernames.get(connection, None)
            if user_name and current_user_name is not None and user_name == current_user_name:
                continue
            try:
                await connection.send_text(message)
            except websockets.exceptions.ConnectionClosed as e:
                print(f"{current_user_name} connection closed: {connection}")
                if connection in self.active_connections:
                    self.active_connections.remove(connection)
                else:
                    print(f"{current_user_name} connection is removed")


manager = ConnectionManager()


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            message = f"{username}: {data}"
            await manager.broadcast(message)
    except WebSocketDisconnect:
        user_name = manager.disconnect(websocket)
        await manager.broadcast(f"{user_name} left the chat")
    except Exception as e:
        print(f"Other exception: {traceback.format_exc()}")


@app.get("/{username}")
async def index(username):
    return {"name": username}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, log_level="info", reload=False)
