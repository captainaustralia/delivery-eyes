import datetime
import os

SECRET_KEY = os.environ.get("SECRET", "test")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
    "ACCESS_TOKEN_EXPIRE_TIME", datetime.timedelta(minutes=30)
)
REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get(
    "REFRESH_TOKEN_EXPIRE_TIME", datetime.timedelta(seconds=1)
)
