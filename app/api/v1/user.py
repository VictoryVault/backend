from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError

from app.core.database import get_db
from app.core.auth import oauth2_scheme
from app.models.user import UserRead, UserCreate
import app.crud.user as crud_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/get-user", response_model=UserRead | None)
async def get_user(
        id: str, 
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db), 
    ):
    try:
        user = await crud_user.get(db, id)
    except DBAPIError:
        return None

    return user


@router.get("/get-users", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await crud_user.get_all(db)
    return users


@router.post("/create-user", response_model=UserRead | None)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud_user.create(db, user)
    return user
