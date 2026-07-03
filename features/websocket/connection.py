from fastapi import WebSocket
from starlette.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        # trip_id -> user_id -> websocket
        self.active_connections: dict[str, dict[str, WebSocket]] = {}

        # trip_id -> user state
        self.user_state: dict[str, dict[str, str]] = {}
        # status: online / offline / left

    async def connect(self, websocket: WebSocket, trip_id: str, user_id: str):
        await websocket.accept()

        if trip_id not in self.active_connections:
            self.active_connections[trip_id] = {}
            self.user_state[trip_id] = {}

        self.active_connections[trip_id][user_id] = websocket
        self.user_state[trip_id][user_id] = "online"

        print(f"✅ CONNECT {trip_id} - {user_id}")

    def disconnect(self, trip_id: str, user_id: str):
        if trip_id in self.active_connections:
            self.active_connections[trip_id].pop(user_id, None)

            # ❗ disconnect = offline, NOT leave
            if trip_id in self.user_state:
                self.user_state[trip_id][user_id] = "offline"

            if not self.active_connections[trip_id]:
                del self.active_connections[trip_id]

        print(f"⚠️ DISCONNECT (offline) {trip_id} - {user_id}")

    def leave(self, trip_id: str, user_id: str):
        """User intentionally leaves trip"""
        if trip_id in self.active_connections:
            self.active_connections[trip_id].pop(user_id, None)

        if trip_id in self.user_state:
            self.user_state[trip_id][user_id] = "left"

        print(f"🚪 LEAVE {trip_id} - {user_id}")

    async def broadcast(self, trip_id: str, message: dict):
        if trip_id not in self.active_connections:
            return

        for ws in self.active_connections[trip_id].values():
            if ws.client_state == WebSocketState.CONNECTED:
                await ws.send_json(message)


manager = ConnectionManager()