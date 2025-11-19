"""Authentication routes: register and token endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas, db, models, auth

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead)
async def register_user(user_in: schemas.UserCreate, session: AsyncSession = Depends(db.get_session)):
    q = await session.execute(models.User.__table__.select().where(models.User.username == user_in.username))
    if q.first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = auth.get_password_hash(user_in.password)
    user = models.User(username=user_in.username, hashed_password=hashed)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return schemas.UserRead(id=user.id, username=user.username, is_active=user.is_active, role=user.role)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db.get_session)):
    q = await session.execute(models.User.__table__.select().where(models.User.username == form_data.username))
    row = q.first()
    if not row:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = row[0]
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
