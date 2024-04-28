from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import UserRead, UserCreate
import app.crud.user as crud_user


# router which all routes in this file are relative to
# routers all get imported into the main app in main.py
router = APIRouter(prefix="/users", tags=["users"])


# route with example of path parameter (called e.g. GET .../users/1234)
@router.get("/{user_id}", response_model=UserRead | None)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get(db, user_id)
    return user


@router.get("/", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await crud_user.get_all(db)
    return users


@router.post("/", response_model=UserRead | None)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud_user.create(db, user)
    return user
