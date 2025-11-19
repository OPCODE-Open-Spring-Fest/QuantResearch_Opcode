"""Backtest endpoints: enqueue backtest jobs and fetch results."""

from __future__ import annotations

import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .. import auth, db, models, schemas
from ..tasks.celery_app import celery_app
from ..utils.ws_manager import manager

router = APIRouter(prefix="/api/backtest", tags=["backtest"])


@router.post("/", response_model=schemas.BacktestStatus)
async def submit_backtest(
    req: schemas.BacktestRequest,
    current_user=Depends(auth.require_active_user),
    session: AsyncSession = Depends(db.get_session),
):
    # Create job
    job_id = uuid.uuid4().hex
    job = models.BacktestJob(
        id=job_id, user_id=current_user.id, status="queued", params=req.dict()
    )
    session.add(job)
    await session.commit()

    # Enqueue celery task
    celery_app.send_task(
        "quant_research_starter.api.tasks.tasks.run_backtest", args=[job_id, req.dict()]
    )

    return {"job_id": job_id, "status": "queued"}


@router.get("/{job_id}/results")
async def get_results(
    job_id: str,
    current_user=Depends(auth.require_active_user),
    session: AsyncSession = Depends(db.get_session),
):
    q = await session.execute(
        models.BacktestJob.__table__.select().where(models.BacktestJob.id == job_id)
    )
    row = q.first()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    job = row[0]
    if job.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this job")

    if job.result_path and os.path.exists(job.result_path):
        import json

        with open(job.result_path, "r") as f:
            return json.load(f)
    return {"status": job.status}


@router.websocket("/ws/{job_id}")
async def websocket_backtest(websocket: WebSocket, job_id: str):
    """WebSocket endpoint that registers the client and relays messages from Redis pub/sub.

    The Redis listener broadcasts messages to the ConnectionManager which then sends
    them to connected WebSocket clients.
    """
    await manager.connect(job_id, websocket)
    try:
        while True:
            # keep the connection alive; client may send ping messages
            msg = await websocket.receive_text()
            # ignore incoming messages; server pushes updates
            await websocket.send_text("ok")
    except Exception:
        manager.disconnect(job_id, websocket)
        try:
            await websocket.close()
        except Exception:
            pass
