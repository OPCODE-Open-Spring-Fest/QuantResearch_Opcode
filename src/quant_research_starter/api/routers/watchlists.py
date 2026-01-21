"""Watchlist management endpoints."""

from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc

from ..auth import get_current_user
from ..db import get_session
from ..models import User, Watchlist
from ..schemas import WatchlistCreate, WatchlistUpdate, WatchlistAddSymbol, WatchlistResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/watchlists", tags=["watchlists"])


@router.post("/", response_model=WatchlistResponse, status_code=status.HTTP_201_CREATED)
async def create_watchlist(
    request: WatchlistCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new watchlist."""
    try:
        # Uppercase all symbols
        symbols = [s.upper() for s in request.symbols]
        
        watchlist = Watchlist(
            user_id=current_user.id,
            name=request.name,
            description=request.description,
            symbols=symbols
        )
        
        db.add(watchlist)
        await db.commit()
        await db.refresh(watchlist)
        
        return {
            "id": watchlist.id,
            "name": watchlist.name,
            "description": watchlist.description,
            "symbols": watchlist.symbols,
            "created_at": watchlist.created_at.isoformat(),
            "updated_at": watchlist.updated_at.isoformat()
        }
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating watchlist: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create watchlist: {str(e)}"
        )


@router.get("/", response_model=List[WatchlistResponse])
async def get_watchlists(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all watchlists for the current user."""
    try:
        result = await db.execute(
            select(Watchlist)
            .where(Watchlist.user_id == current_user.id)
            .order_by(desc(Watchlist.created_at))
        )
        watchlists = result.scalars().all()
        
        return [
            {
                "id": w.id,
                "name": w.name,
                "description": w.description,
                "symbols": w.symbols,
                "created_at": w.created_at.isoformat(),
                "updated_at": w.updated_at.isoformat()
            }
            for w in watchlists
        ]
    except Exception as e:
        logger.error(f"Error fetching watchlists: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch watchlists: {str(e)}"
        )


@router.get("/{watchlist_id}", response_model=WatchlistResponse)
async def get_watchlist(
    watchlist_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific watchlist by ID."""
    try:
        result = await db.execute(
            select(Watchlist).where(
                and_(
                    Watchlist.id == watchlist_id,
                    Watchlist.user_id == current_user.id
                )
            )
        )
        watchlist = result.scalar_one_or_none()
        
        if not watchlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Watchlist not found"
            )
        
        return {
            "id": watchlist.id,
            "name": watchlist.name,
            "description": watchlist.description,
            "symbols": watchlist.symbols,
            "created_at": watchlist.created_at.isoformat(),
            "updated_at": watchlist.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching watchlist {watchlist_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch watchlist: {str(e)}"
        )


@router.put("/{watchlist_id}", response_model=WatchlistResponse)
async def update_watchlist(
    watchlist_id: int,
    request: WatchlistUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a watchlist."""
    try:
        result = await db.execute(
            select(Watchlist).where(
                and_(
                    Watchlist.id == watchlist_id,
                    Watchlist.user_id == current_user.id
                )
            )
        )
        watchlist = result.scalar_one_or_none()
        
        if not watchlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Watchlist not found"
            )
        
        # Update fields
        if request.name is not None:
            watchlist.name = request.name
        if request.description is not None:
            watchlist.description = request.description
        
        await db.commit()
        await db.refresh(watchlist)
        
        return {
            "id": watchlist.id,
            "name": watchlist.name,
            "description": watchlist.description,
            "symbols": watchlist.symbols,
            "created_at": watchlist.created_at.isoformat(),
            "updated_at": watchlist.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating watchlist {watchlist_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update watchlist: {str(e)}"
        )


@router.delete("/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watchlist(
    watchlist_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a watchlist."""
    try:
        result = await db.execute(
            select(Watchlist).where(
                and_(
                    Watchlist.id == watchlist_id,
                    Watchlist.user_id == current_user.id
                )
            )
        )
        watchlist = result.scalar_one_or_none()
        
        if not watchlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Watchlist not found"
            )
        
        await db.delete(watchlist)
        await db.commit()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting watchlist {watchlist_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete watchlist: {str(e)}"
        )


@router.post("/{watchlist_id}/symbols")
async def add_symbol_to_watchlist(
    watchlist_id: int,
    request: WatchlistAddSymbol,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Add a symbol to a watchlist."""
    try:
        result = await db.execute(
            select(Watchlist).where(
                and_(
                    Watchlist.id == watchlist_id,
                    Watchlist.user_id == current_user.id
                )
            )
        )
        watchlist = result.scalar_one_or_none()
        
        if not watchlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Watchlist not found"
            )
        
        symbol = request.symbol.upper()
        
        # Check if symbol already exists
        if symbol in watchlist.symbols:
            return {
                "status": "info",
                "message": f"{symbol} is already in watchlist '{watchlist.name}'",
                "watchlist_id": watchlist.id
            }
        
        # Add symbol
        watchlist.symbols.append(symbol)
        await db.commit()
        
        return {
            "status": "success",
            "message": f"Added {symbol} to watchlist '{watchlist.name}'",
            "watchlist_id": watchlist.id,
            "symbols": watchlist.symbols
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error adding symbol to watchlist {watchlist_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add symbol to watchlist: {str(e)}"
        )


@router.delete("/{watchlist_id}/symbols/{symbol}")
async def remove_symbol_from_watchlist(
    watchlist_id: int,
    symbol: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Remove a symbol from a watchlist."""
    try:
        result = await db.execute(
            select(Watchlist).where(
                and_(
                    Watchlist.id == watchlist_id,
                    Watchlist.user_id == current_user.id
                )
            )
        )
        watchlist = result.scalar_one_or_none()
        
        if not watchlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Watchlist not found"
            )
        
        symbol = symbol.upper()
        
        # Check if symbol exists
        if symbol not in watchlist.symbols:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{symbol} not found in watchlist"
            )
        
        # Remove symbol
        watchlist.symbols.remove(symbol)
        await db.commit()
        
        return {
            "status": "success",
            "message": f"Removed {symbol} from watchlist '{watchlist.name}'",
            "watchlist_id": watchlist.id,
            "symbols": watchlist.symbols
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error removing symbol from watchlist {watchlist_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove symbol from watchlist: {str(e)}"
        )
