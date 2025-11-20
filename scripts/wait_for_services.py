#!/usr/bin/env python3
"""Wait for dependent services (Postgres, Redis) to be ready.

This helper is used as part of the Docker entrypoint to ensure services
are available before starting the web server or worker.
"""
import os
import socket
import sys
import time


def wait_tcp(host: str, port: int, timeout: int = 60) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except Exception:
            time.sleep(1)
    return False


def main():
    db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@db:5432/qrs")
    # parse host and port in the common pattern
    # support postgresql+asyncpg://user:pass@host:port/db
    try:
        after_at = db_url.split("@", 1)[1]
        hostport = after_at.split("/", 1)[0]
        host, port = hostport.split(":")
        port = int(port)
    except Exception:
        host, port = ("db", 5432)

    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    try:
        rafter = redis_url.split("//", 1)[1]
        rhostport = rafter.split("/", 1)[0]
        rhost, rport = rhostport.split(":")
        rport = int(rport)
    except Exception:
        rhost, rport = ("redis", 6379)

    print(f"Waiting for postgres at {host}:{port}...")
    if not wait_tcp(host, port, timeout=60):
        print("Postgres did not become available in time.")
        sys.exit(1)

    print(f"Waiting for redis at {rhost}:{rport}...")
    if not wait_tcp(rhost, rport, timeout=30):
        print("Redis did not become available in time.")
        sys.exit(1)

    print("All services are available.")


if __name__ == "__main__":
    main()
