from fastapi import WebSocket
from starlette.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        # trip_id -> user_id -> websocket
        self.active_connections: dict[str, dict[str, WebSocket]] = {}

        # trip_id -> user_id -> state object
        self.user_state: dict[str, dict[str, dict]] = {}
        # status: ACTIVE / PAUSED / OFFLINE / LEFT

        # print(self)

    async def connect(self, websocket: WebSocket, trip_id: str, user_id: str):
        await websocket.accept()

        if trip_id not in self.active_connections:
            self.active_connections[trip_id] = {}
            self.user_state[trip_id] = {}

        self.active_connections[trip_id][user_id] = websocket

        # ⚡ connect 不等於 active（等 start message 才算）
        self.user_state[trip_id][user_id] = {
            "status": "CONNECTED",
            "last_location": None
        }

        print(f"✅ CONNECT {trip_id} - {user_id}")

    # -------------------------
    # START RIDE
    # -------------------------
    def start(self, trip_id: str, user_id: str):
        self._ensure_user(trip_id, user_id)

        self.user_state[trip_id][user_id]["status"] = "ACTIVE"
        print(f"[ACTIVE] {trip_id} - {user_id}")

    # -------------------------
    # PAUSE RIDE
    # -------------------------
    def pause(self, trip_id: str, user_id: str):
        self._ensure_user(trip_id, user_id)

        self.user_state[trip_id][user_id]["status"] = "PAUSED"
        print(f"[PAUSED] {trip_id} - {user_id}")

    # -------------------------
    # UPDATE LOCATION
    # -------------------------
    def update_location(self, trip_id: str, user_id: str, location: dict):
        self._ensure_user(trip_id, user_id)

        if self.user_state[trip_id][user_id]["status"] != "ACTIVE":
            return  # paused / offline / left 不更新

        self.user_state[trip_id][user_id]["last_location"] = location

    # -------------------------
    # LEAVE TRIP
    # -------------------------
    def leave(self, trip_id: str, user_id: str):
        if trip_id in self.active_connections:
            self.active_connections[trip_id].pop(user_id, None)

        if trip_id in self.user_state:
            self.user_state[trip_id][user_id]["status"] = "LEFT"

        print(f"[LEFT] {trip_id} - {user_id}")

    # -------------------------
    # DISCONNECT (network)
    # -------------------------
    def disconnect(self, trip_id: str, user_id: str):
        if trip_id in self.active_connections:
            self.active_connections[trip_id].pop(user_id, None)

        if trip_id in self.user_state:
            if user_id in self.user_state[trip_id]:
                self.user_state[trip_id][user_id]["status"] = "OFFLINE"

        print(f"[OFFLINE] {trip_id} - {user_id}")

    # -------------------------
    # BROADCAST
    # -------------------------
    async def broadcast(self, trip_id: str, message: dict):
        if trip_id not in self.active_connections:
            return

        for ws in self.active_connections[trip_id].values():
            if ws.client_state == WebSocketState.CONNECTED:
                await ws.send_json(message)

    # -------------------------
    # helper
    # -------------------------
    def _ensure_user(self, trip_id: str, user_id: str):
        if trip_id not in self.user_state:
            self.user_state[trip_id] = {}

        if user_id not in self.user_state[trip_id]:
            self.user_state[trip_id][user_id] = {
                "status": "OFFLINE",
                "last_location": None
            }


manager = ConnectionManager()