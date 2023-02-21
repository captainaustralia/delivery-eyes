from fastapi import FastAPI
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes
)

from jwt_auth.auth_router import router

app = FastAPI()
app.include_router(router=router)
