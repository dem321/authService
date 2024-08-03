from datetime import datetime, UTC, timedelta

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from config import Config
from repositories.user import UserRepository
from schemas.user import UserRetrieveSchema

import jwt


class UserService:

    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository()

    async def login(self, email: str, password: str, db: AsyncSession) -> JSONResponse:

        user = await self.user_repository.get_user_by_email(email=email, db=db)
        if not user:
            return JSONResponse({'error': 'Wrong email or password'}, status_code=404)

        if not bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
            return JSONResponse({'error': 'Wrong email or password'}, status_code=404)

        with open(Config.JWT_PRIVATE_KEY, 'r') as f:
            private_key = f.read()

        access_token = jwt.encode({'id': user.id, 'exp': datetime.now(UTC) + timedelta(hours=2),
                                   'roles': user.role, 'name': user.name, 'email': user.email},
                                  private_key, 'RS256')

        refresh_token = jwt.encode({'id': user.id, 'exp': datetime.now(UTC) + timedelta(days=7),
                                    'roles': user.role, 'name': user.name, 'email': user.email},
                                   private_key, 'RS256')

        response = JSONResponse({'status': 'success', 'user': UserRetrieveSchema(**user.__dict__)})
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=timedelta(days=7).seconds)
        response.headers['Authorization'] = f'Bearer {access_token}'
        return response
