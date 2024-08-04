from typing import Annotated

from fastapi import APIRouter, Cookie
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from services.user import UserService

from schemas.user import UserCreateSchema, BaseUserSchema, UserRetrieveSchema

router = APIRouter()

user_service = UserService()


@router.post("/api/v0/login")
async def login(email: str, password: str, db: AsyncSession) -> JSONResponse:
    if not email or not password:
        return JSONResponse({"error": "Email or password is empty"}, status_code=400)
    return await user_service.login(email, password, db)


@router.post("/api/v0/logout")
async def logout() -> JSONResponse:
    return await user_service.logout()


@router.post("/api/v0/register", response_model=BaseUserSchema)
async def register(user: UserCreateSchema, db: AsyncSession) -> User:
    return await user_service.register(user, db)


@router.post("/api/v0/update-token")
async def update_token(refresh_token: Annotated[str, Cookie()], db: AsyncSession) -> JSONResponse:
    return await user_service.update_token(refresh_token, db)


# @router.get("/api/v0/user/self")
# async def get_user() -> JSONResponse:
#     return await user_service.get_user_self(db: AsyncSession) -> UserRetrieveSchema:
#     pass