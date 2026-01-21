"""Alert management endpoints."""

from __future__ import annotations

import logging
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc

from ..auth import get_current_user
from ..db import get_session
from ..models import User, Alert, StockQuote
from ..schemas import AlertCreate, AlertUpdate, AlertResponse
from ..services.finnhub import FinnhubService
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


def get_finnhub_service() -> FinnhubService:
    """Dependency to get Finnhub service."""
    api_key = os.getenv("FINNHUB_API_KEY", "test_key")
    return FinnhubService(api_key)


@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    request: AlertCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Create a new price alert."""
    try:
        # Get current price
        quote = await finnhub_service.update_cached_quote(db, request.symbol)
        current_value = quote.current_price if quote else None
        
        alert = Alert(
            user_id=current_user.id,
            symbol=request.symbol.upper(),
            alert_type=request.alert_type,
            threshold_value=request.threshold_value,
            current_value=current_value,
            message=request.message,
            is_active=request.is_active
        )
        
        db.add(alert)
        await db.commit()
        await db.refresh(alert)
        
        return {
            "id": alert.id,
            "symbol": alert.symbol,
            "alert_type": alert.alert_type,
            "threshold_value": alert.threshold_value,
            "current_value": alert.current_value,
            "message": alert.message,
            "is_active": alert.is_active,
            "triggered_at": alert.triggered_at.isoformat() if alert.triggered_at else None,
            "created_at": alert.created_at.isoformat()
        }
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating alert: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create alert: {str(e)}"
        )


@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    active_only: bool = False,
    symbol: str = None,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all alerts for the current user."""
    try:
        query = select(Alert).where(Alert.user_id == current_user.id)
        
        if active_only:
            query = query.where(Alert.is_active == True)
        
        if symbol:
            query = query.where(Alert.symbol == symbol.upper())
        
        query = query.order_by(desc(Alert.created_at))
        
        result = await db.execute(query)
        alerts = result.scalars().all()
        
        return [
            {
                "id": a.id,
                "symbol": a.symbol,
                "alert_type": a.alert_type,
                "threshold_value": a.threshold_value,
                "current_value": a.current_value,
                "message": a.message,
                "is_active": a.is_active,
                "triggered_at": a.triggered_at.isoformat() if a.triggered_at else None,
                "created_at": a.created_at.isoformat()
            }
            for a in alerts
        ]
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch alerts: {str(e)}"
        )


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific alert by ID."""
    try:
        result = await db.execute(
            select(Alert).where(
                and_(
                    Alert.id == alert_id,
                    Alert.user_id == current_user.id
                )
            )
        )
        alert = result.scalar_one_or_none()
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        
        return {
            "id": alert.id,
            "symbol": alert.symbol,
            "alert_type": alert.alert_type,
            "threshold_value": alert.threshold_value,
            "current_value": alert.current_value,
            "message": alert.message,
            "is_active": alert.is_active,
            "triggered_at": alert.triggered_at.isoformat() if alert.triggered_at else None,
            "created_at": alert.created_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching alert {alert_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch alert: {str(e)}"
        )


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    request: AlertUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update an alert."""
    try:
        result = await db.execute(
            select(Alert).where(
                and_(
                    Alert.id == alert_id,
                    Alert.user_id == current_user.id
                )
            )
        )
        alert = result.scalar_one_or_none()
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        
        # Update fields
        if request.threshold_value is not None:
            alert.threshold_value = request.threshold_value
        if request.message is not None:
            alert.message = request.message
        if request.is_active is not None:
            alert.is_active = request.is_active
        
        await db.commit()
        await db.refresh(alert)
        
        return {
            "id": alert.id,
            "symbol": alert.symbol,
            "alert_type": alert.alert_type,
            "threshold_value": alert.threshold_value,
            "current_value": alert.current_value,
            "message": alert.message,
            "is_active": alert.is_active,
            "triggered_at": alert.triggered_at.isoformat() if alert.triggered_at else None,
            "created_at": alert.created_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating alert {alert_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update alert: {str(e)}"
        )


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete an alert."""
    try:
        result = await db.execute(
            select(Alert).where(
                and_(
                    Alert.id == alert_id,
                    Alert.user_id == current_user.id
                )
            )
        )
        alert = result.scalar_one_or_none()
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        
        await db.delete(alert)
        await db.commit()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting alert {alert_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete alert: {str(e)}"
        )


@router.post("/check")
async def check_alerts(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Check all active alerts and trigger if conditions are met."""
    try:
        # Get all active alerts
        result = await db.execute(
            select(Alert).where(
                and_(
                    Alert.user_id == current_user.id,
                    Alert.is_active == True
                )
            )
        )
        alerts = result.scalars().all()
        
        triggered_alerts = []
        
        for alert in alerts:
            # Get current price
            quote = await finnhub_service.update_cached_quote(db, alert.symbol)
            if not quote:
                continue
            
            current_price = quote.current_price
            alert.current_value = current_price
            
            # Check if alert should trigger
            should_trigger = False
            
            if alert.alert_type == "price_above" and current_price >= alert.threshold_value:
                should_trigger = True
            elif alert.alert_type == "price_below" and current_price <= alert.threshold_value:
                should_trigger = True
            elif alert.alert_type == "percent_change":
                percent_change = abs(quote.percent_change)
                if percent_change >= alert.threshold_value:
                    should_trigger = True
            
            if should_trigger:
                alert.triggered_at = datetime.utcnow()
                alert.is_active = False  # Deactivate after triggering
                triggered_alerts.append({
                    "id": alert.id,
                    "symbol": alert.symbol,
                    "alert_type": alert.alert_type,
                    "threshold_value": alert.threshold_value,
                    "current_value": current_price,
                    "message": alert.message or f"{alert.symbol} alert triggered"
                })
        
        await db.commit()
        
        return {
            "status": "success",
            "checked": len(alerts),
            "triggered": len(triggered_alerts),
            "alerts": triggered_alerts
        }
    except Exception as e:
        await db.rollback()
        logger.error(f"Error checking alerts: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check alerts: {str(e)}"
        )
