"""Authentication routes: register and token endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .. import auth, db, models, schemas, supabase

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead)
async def register_user(
    user_in: schemas.UserCreate,
    session: Annotated[AsyncSession, Depends(db.get_session)],
):
    # If Supabase is configured, forward signup to Supabase and then create
    # a local mapping record for the user (so other resources keep integer IDs).
    if supabase.is_enabled():
        try:
            supabase.signup(user_in.username, user_in.password)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    q = await session.execute(
        models.User.__table__.select().where(models.User.username == user_in.username)
    )
    if q.first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = auth.get_password_hash(user_in.password)
    user = models.User(username=user_in.username, hashed_password=hashed)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return schemas.UserRead(
        id=user.id, username=user.username, is_active=user.is_active, role=user.role
    )


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(db.get_session)],
):
    # If Supabase is enabled, use Supabase to obtain token
    if supabase.is_enabled():
        try:
            token_response = supabase.sign_in(form_data.username, form_data.password)
            # token_response may contain access_token and refresh_token
            return {"access_token": token_response.get("access_token"), "token_type": "bearer"}
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    q = await session.execute(
        models.User.__table__.select().where(models.User.username == form_data.username)
    )
    row = q.first()
    if not row:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = row[0]
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
