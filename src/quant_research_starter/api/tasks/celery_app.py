"""Celery application configuration."""

import os
import ssl
from pathlib import Path

from celery import Celery
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Configure broker with SSL if needed
broker_use_ssl = None
if REDIS_URL.startswith("rediss://"):
    broker_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE,
        'ssl_check_hostname': False,
    }

celery_app = Celery(
    "qrs_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

if broker_use_ssl:
    celery_app.conf.broker_use_ssl = broker_use_ssl
    celery_app.conf.redis_backend_use_ssl = broker_use_ssl

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
