from datetime import datetime, UTC, timedelta

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from config import Config
from models.user import User
from repositories.user import UserRepository
from schemas.user import UserRetrieveSchema, UserCreateSchema

import jwt


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()
        with open(Config.JWT_PRIVATE_KEY, 'r') as f:
            self.private_key = f.read()

    async def login(self, email: str, password: str, db: AsyncSession) -> JSONResponse:

        user = await self.user_repository.get_user_by_email(email=email, db=db)
        if not user:
            return JSONResponse({'error': 'Wrong email or password'}, status_code=404)

        if not bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
            return JSONResponse({'error': 'Wrong email or password'}, status_code=404)

        access_token = jwt.encode({'id': user.id, 'exp': datetime.now(UTC) + timedelta(hours=2),
                                   'roles': user.role, 'first_name': user.first_name, 'last_name': user.last_name,
                                   'middle_name': user.middle_name, 'email': user.email},
                                  self.private_key, 'RS256')

        refresh_token = jwt.encode({'id': user.id, 'exp': datetime.now(UTC) + timedelta(days=7),
                                    'roles': user.role, 'first_name': user.first_name, 'last_name': user.last_name,
                                    'middle_name': user.middle_name, 'email': user.email},
                                   self.private_key, 'RS256')

        response = JSONResponse({'status': 'success', 'user': UserRetrieveSchema(**user.__dict__)})
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=timedelta(days=7).seconds)
        response.headers['Authorization'] = f'Bearer {access_token}'
        return response

    async def register(self, user: UserCreateSchema, db: AsyncSession) -> User:

        user = await self.user_repository.create_user(user=user, db=db)
        return user

    async def logout(self) -> JSONResponse:
        response = JSONResponse({'status': 'success'}, status_code=200)
        response.delete_cookie('refresh_token')
        response.headers['Authorization'] = 'Bearer '
        return response

    async def update_token(self, refresh_token: str, db: AsyncSession) -> JSONResponse:
        user_info = jwt.decode(refresh_token, Config.JWT_PRIVATE_KEY, algorithms=['RS256'])
        user = await self.user_repository.get_user_by_id(user_id=user_info['id'], db=db)
        if not user:
            response = JSONResponse({'status': 'error', 'details': 'invalid_credentials'}, status_code=404)
            response.delete_cookie('refresh_token')
            return response

        access_token = jwt.encode({'id': user.id, 'exp': datetime.now(UTC) + timedelta(hours=2),
                                   'roles': user.role, 'first_name': user.first_name, 'last_name': user.last_name,
                                   'middle_name': user.middle_name, 'email': user.email},
                                  self.private_key, 'RS256')
        response = JSONResponse({'status': 'success', 'user': UserRetrieveSchema(**user.__dict__)})
        response.headers['Authorization'] = f'Bearer {access_token}'

        return response
