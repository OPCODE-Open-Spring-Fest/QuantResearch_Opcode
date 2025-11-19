"""WebSocket manager and Redis subscription helper.

This module provides a simple in-memory WebSocket manager and a Redis-backed
pub/sub helper for broadcasting messages from Celery workers to connected clients.
"""
from typing import Dict, Set
import asyncio
import json
import os

from fastapi import WebSocket
import aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, Set[WebSocket]] = {}

    async def connect(self, job_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active.setdefault(job_id, set()).add(websocket)

    def disconnect(self, job_id: str, websocket: WebSocket):
        if job_id in self.active:
            self.active[job_id].discard(websocket)

    async def broadcast(self, job_id: str, message: str):
        conns = list(self.active.get(job_id, []))
        for ws in conns:
            try:
                await ws.send_text(message)
            except Exception:
                pass


manager = ConnectionManager()


async def redis_listener_loop():
    redis = aioredis.from_url(REDIS_URL)
    pubsub = redis.pubsub()
    await pubsub.psubscribe("backtest:*")

    async for message in pubsub.listen():
        if message is None:
            await asyncio.sleep(0.01)
            continue
        # message format: {'type': 'pmessage', 'pattern': b'backtest:*', 'channel': b'backtest:JOBID', 'data': b'...'}
        if message.get("type") in ("message", "pmessage"):
            ch = message.get("channel") or message.get("pattern")
            if isinstance(ch, bytes):
                ch = ch.decode()
            # channel expected like backtest:JOBID
            parts = ch.split(":", 1)
            if len(parts) == 2:
                _, job_id = parts
                data = message.get("data")
                if isinstance(data, bytes):
                    try:
                        payload = data.decode()
                    except Exception:
                        payload = json.dumps({"data": str(data)})
                else:
                    payload = json.dumps({"data": str(data)})
                await manager.broadcast(job_id, payload)
