from fastapi import APIRouter
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services.user import UserService

router = APIRouter()

user_service = UserService()


@router.post("/api/v0/login")
async def login(email: str, password: str, db: AsyncSession) -> JSONResponse:
    if not email or not password:
        return JSONResponse({"error": "Email or password is empty"}, status_code=400)
    return await user_service.login(email, password, db)


@router.post("/api/v0/logout")
async def logout():
    pass


@router.post("/api/v0/register")
async def register():
    pass
