from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from jwt_auth.base.base_jwt import JWTInterface
from jwt_auth.base.depends import get_db
from jwt_auth.base.schemas import (AccessToken, JWTUserSchema, RefreshToken,
                                   TokenPair)

router = APIRouter(
    prefix="/jwt", tags=["AUTH"]
)


@router.post("/get_pair/", response_model=Optional[TokenPair])
async def get_token_pair(
    session: Session = Depends(get_db), *, user_in: JWTUserSchema
) -> Optional[TokenPair]:
    interface = JWTInterface(session=session, **user_in.dict())
    return await interface.get_pair_token()


@router.post("/refresh/", response_model=Optional[AccessToken])
async def get_new_access(
    session: Session = Depends(get_db), *, token_in: RefreshToken
) -> Optional[AccessToken]:
    interface = JWTInterface(session=session, **token_in.dict())
    return interface.get_access_token()
