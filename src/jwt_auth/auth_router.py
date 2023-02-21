from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from jwt_auth.depends import get_db
from jwt_auth.schemas import Token, JWTUserAuth
from jwt_auth.services import get_jwt_token, get_jwt_refresh

router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.post("/access/", response_model=Optional[Token])
async def get_token_pair(session: Session = Depends(get_db), *, user_in: JWTUserAuth) -> Optional[Token]:
    token = await get_jwt_token(session, user_in)
    return token


@router.post("/refresh/", response_model=Optional[Token])
async def get_refresh_token(session: Session = Depends(get_db), *, user_in: JWTUserAuth) -> Optional[Token]:
    token = await get_jwt_refresh(session, user_in)
    return token
