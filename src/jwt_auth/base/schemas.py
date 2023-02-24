from pydantic import BaseModel


class JWTUserSchema(BaseModel):
    username: str
    password: str


class RefreshToken(BaseModel):
    refresh: str


class AccessToken(BaseModel):
    access: str


class TokenPair(BaseModel):
    access: str
    refresh: str
