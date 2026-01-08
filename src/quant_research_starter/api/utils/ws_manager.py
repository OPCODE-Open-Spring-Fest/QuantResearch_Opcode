"""WebSocket manager and Redis subscription helper.

This module provides a simple in-memory WebSocket manager and a Redis-backed
pub/sub helper for broadcasting messages from Celery workers to connected clients.
"""

import asyncio
import json
import os
import ssl
from typing import Dict, Set

import redis.asyncio as redis
from fastapi import WebSocket

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create SSL context for Redis if using rediss://
def get_redis_client():
    """Create Redis client with proper SSL configuration for Aiven."""
    if REDIS_URL.startswith("rediss://"):
        # Use SSL for Aiven and other cloud Redis providers
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return redis.from_url(
            REDIS_URL, 
            ssl_cert_reqs=ssl.CERT_NONE,
            ssl_check_hostname=False,
            decode_responses=False
        )
    else:
        return redis.from_url(REDIS_URL, decode_responses=False)


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
    """Listen to Redis pub/sub for backtest updates. Fails gracefully if Redis unavailable."""
    try:
        r = get_redis_client()
        pubsub = r.pubsub()
        await pubsub.psubscribe("backtest:*")
        print(f"✅ Redis listener connected successfully to {REDIS_URL.split('@')[1] if '@' in REDIS_URL else 'Redis'}")
    except Exception as e:
        print(f"⚠️  Redis connection failed (WebSocket real-time updates disabled): {str(e)[:100]}")
        print("   The API will work normally, but live backtest progress won't be available.")
        return  # Exit gracefully - API continues to work

    try:
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
    except Exception as e:
        print(f"⚠️  Redis listener encountered an error: {e}")
        # Listener will restart on next application reload
