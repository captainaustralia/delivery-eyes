from sqlalchemy import select
from sqlalchemy.orm import Session
from delivery_heart.models import User
from jwt_auth.schemas import JWTUserAuth


async def get_jwt_token(db: Session, user_in: JWTUserAuth):
    q = select(User).where(User.username == user_in.username, User.phone == user_in.password)
    obj = db.execute(q).fetchone()
    if obj:
        pass
    return None


async def get_jwt_refresh(db: Session, user_in: JWTUserAuth):
    q = select(User).where(User.username == user_in.username, User.phone == user_in.password)
    obj = db.execute(q).fetchone()
    if obj:
        pass
    return None
