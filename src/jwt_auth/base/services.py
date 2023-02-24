from typing import Optional

from sqlalchemy.orm import Session

from delivery_heart.models import User
from delivery_heart.schemas import UserWriteSchema
from jwt_auth.base.hasher import get_password_hash


async def get_user(db: Session, username: str) -> Optional[User]:
    user = db.query(User).where(User.username == username).one_or_none()
    return user


async def create_user(db: Session, user_in: UserWriteSchema):
    user = User(**user_in.dict())
    user.password = get_password_hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
