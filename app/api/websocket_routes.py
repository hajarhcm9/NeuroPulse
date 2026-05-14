"""Smart Guardian - WebSocket routes for real-time seizure alerts."""

import logging
import asyncio
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("smart-guardian")

router = APIRouter(tags=["WebSocket"])


class WebSocketManager:
    """Manage WebSocket connections for real-time alert push."""

    def __init__(self):
        self._connections: Dict[int, Set[WebSocket]] = {}
        self._loop = None

    def set_loop(self, loop):
        """Store the main event loop for thread-safe scheduling."""
        self._loop = loop

    async def connect(self, user_id: int, websocket: WebSocket):
        """Accept and register a WebSocket connection."""
        await websocket.accept()
        if user_id not in self._connections:
            self._connections[user_id] = set()
        self._connections[user_id].add(websocket)
        logger.info(
            "WebSocket connected: user=%s connections=%s",
            user_id, len(self._connections[user_id]),
        )

    def disconnect(self, user_id: int, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if user_id in self._connections:
            self._connections[user_id].discard(websocket)
            if not self._connections[user_id]:
                del self._connections[user_id]
        logger.info("WebSocket disconnected: user=%s", user_id)

    def send_to_user(self, user_id: int, data: dict):
        """Thread-safe send: works from MQTT thread or async context."""
        if not self._loop or user_id not in self._connections:
            return
        try:
            asyncio.run_coroutine_threadsafe(
                self._async_send(user_id, data), self._loop
            )
        except Exception as e:
            logger.error("WebSocket send_to_user error: %s", e)

    async def _async_send(self, user_id: int, data: dict):
        """Send data to all connections for a user."""
        connections = self._connections.get(user_id, set())
        dead = set()
        for ws in connections:
            try:
                await ws.send_json(data)
            except Exception:
                dead.add(ws)
        for ws in dead:
            connections.discard(ws)

    @property
    def connection_count(self) -> int:
        """Total active WebSocket connections."""
        return sum(len(c) for c in self._connections.values())


# Singleton manager
ws_manager = WebSocketManager()


@router.websocket("/ws/alerts/{user_id}")
async def websocket_alerts(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time seizure alerts.

    Client connects to: ws://host:8000/ws/alerts/{user_id}
    Server pushes alert JSON when seizure detected.
    Client can send 'ping' to keep alive.
    """
    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, websocket)
    except Exception as e:
        logger.error("WebSocket error user=%s: %s", user_id, e)
        ws_manager.disconnect(user_id, websocket)