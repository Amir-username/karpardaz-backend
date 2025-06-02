from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from ...auth.auth_admin import authenticate_admin
from ...auth.token import Token, create_access_token
from ...config import ACCESS_TOKEN_EXPIRE_MINUTES


admin_router = APIRouter()


@admin_router.post("/admin/login")
async def login_for_access_token_admin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    admin = authenticate_admin(form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
