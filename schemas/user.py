from pydantic import BaseModel


class BaseUserSchema(BaseModel):

    id: int
    name: str
    email: str
    password: str
    role: str


class UserRetrieveSchema(BaseModel):

    id: int
    name: str
    email: str
    role: str


class UserCreateSchema(BaseModel):

    name: str
    email: str
    password: str
    role: str
