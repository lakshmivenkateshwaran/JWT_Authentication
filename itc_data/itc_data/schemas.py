from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    sub: str
