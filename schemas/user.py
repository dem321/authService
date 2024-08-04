import re

from pydantic import BaseModel
from pydantic.v1 import validator


class BaseUserSchema(BaseModel):

    id: int
    first_name: str
    last_name: str
    middle_name: str
    email: str
    password: str
    role: str


class UserRetrieveSchema(BaseModel):

    id: int
    first_name: str
    last_name: str
    middle_name: str
    email: str
    role: str


class UserCreateSchema(BaseModel):

    first_name: str
    last_name: str
    middle_name: str
    email: str
    password: str
    confirm_password: str

    @validator('password')
    def validate_password(cls, password, values):

        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            raise ValueError('Password must contain at least one lowercase letter')

        if password != values['confirm_password']:
            raise ValueError('Passwords do not match')

        return password

    @validator('email')
    def validate_email(cls, email):

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(regex, email):
            raise ValueError('Invalid email address')

        return email


