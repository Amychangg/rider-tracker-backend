from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from features.websocket.connection import manager

router = APIRouter(prefix="/road_map", tags=["road_map"])


@router.websocket("/ws/trip/{trip_id}")
async def road_map(websocket: WebSocket, trip_id: str):

    user_id = websocket.query_params.get("user_id")

    if not user_id:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, trip_id, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            # -------------------------
            # JOIN
            # -------------------------
            if msg_type == "join":
                print(f"👤 {user_id} joined trip {trip_id}")

                await manager.broadcast(trip_id, {
                    "type": "user_joined",
                    "user_id": user_id
                })

            # -------------------------
            # LOCATION UPDATE
            # -------------------------
            elif msg_type == "location":
                data["user_id"] = user_id
                data["trip_id"] = trip_id

                await manager.broadcast(trip_id, data)

            # -------------------------
            # LEAVE TRIP
            # -------------------------
            elif msg_type == "leave":
                print(f"🚪 {user_id} leaving trip {trip_id}")

                manager.leave(trip_id, user_id)

                await manager.broadcast(trip_id, {
                    "type": "user_left",
                    "user_id": user_id
                })

                await websocket.close()
                break

            # -------------------------
            # UNKNOWN TYPE
            # -------------------------
            else:
                await manager.broadcast(trip_id, {
                    "type": "unknown",
                    "message": data
                })

    except WebSocketDisconnect:
        manager.disconnect(trip_id, user_id)
        await manager.broadcast(trip_id, {
            "type": "connection_status",
            "user_id": user_id,
            "connection_status": "offline",
        })