import abc
from datetime import datetime
from typing import Final, Optional, Self

import jose.exceptions
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

import settings.base
from delivery_heart.models import User
from jwt_auth.base.choices import TokenType
from jwt_auth.base.schemas import AccessToken, RefreshToken, TokenPair
from jwt_auth.base.services import get_user


class AbstractTokenInterface(abc.ABC):
    _ACCESS_TIME: Final = settings.base.ACCESS_TOKEN_EXPIRE_MINUTES
    _REFRESH_TIME: Final = settings.base.REFRESH_TOKEN_EXPIRE_MINUTES
    _ALGORITHM: Final = settings.base.ALGORITHM
    _SECRET: Final = settings.base.SECRET_KEY

    _TIME_MAP = {
        TokenType.ACCESS.value: _ACCESS_TIME,
        TokenType.REFRESH.value: _REFRESH_TIME,
    }

    @abc.abstractmethod
    def _make_raw_token(self: Self, token_type: str) -> str:
        ...

    @property
    @abc.abstractmethod
    def get_pair(self: Self) -> TokenPair:
        ...

    @abc.abstractmethod
    def access(self: Self) -> AccessToken:
        ...


class BaseTokenInterface(AbstractTokenInterface):
    def __init__(self, user: Optional[User] = None, refresh: str = None) -> None:
        self._user = user
        self._refresh = refresh
        self._uid = None

    def _make_raw_token(self, token_type: TokenType) -> str:
        expire_time = datetime.utcnow() + self._TIME_MAP[token_type.value]
        raw_token = jwt.encode(
            claims={"uid": self._uid or str(self._user.uid), "exp": expire_time},
            key=self._SECRET,
            algorithm=self._ALGORITHM,
        )
        return raw_token

    def get_pair(self) -> TokenPair:
        return TokenPair(
            access=self._make_raw_token(TokenType.ACCESS),
            refresh=self._make_raw_token(TokenType.REFRESH),
        )

    def access(self):
        try:
            raw_info: dict = jwt.decode(self._refresh, self._SECRET, self._ALGORITHM)
        except jose.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="TOKEN EXPIRED")
        except jose.exceptions.JWTError:
            raise HTTPException(status_code=403)
        self._uid = raw_info.get("uid")
        return AccessToken(access=self._make_raw_token(TokenType.ACCESS))


class JWTInterface:
    def __init__(
        self: Self,
        session: Session,
        password: Optional[str] = None,
        username: Optional[str] = None,
        refresh: Optional[str] = None,
    ) -> None:
        self._password = password
        self._username = username

        self._session: Optional[Session] = session
        self._refresh: Optional[RefreshToken] = refresh
        self._user: Optional[User] = None

    async def get_pair_token(self):
        if await self._check_password():
            return BaseTokenInterface(user=self._user).get_pair()
        raise HTTPException(status_code=403)

    def get_access_token(self):
        return BaseTokenInterface(refresh=self._refresh).access()

    async def _check_password(self) -> bool:
        await self._get_exist_user()
        return self._user.check_password(self._password)

    async def _get_exist_user(self) -> None:
        user = await get_user(self._session, self._username)
        if user:
            self._user = user
        else:
            raise HTTPException(detail="", status_code=400)
