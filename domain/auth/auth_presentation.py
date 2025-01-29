from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from domain.auth.authentication_service import authenticate_user, create_access_token, create_refresh_token, get_current_active_user
from domain.user.user_schema import UserPrivate


router = APIRouter(prefix="/auth", tags=["auth"])
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    #implementer la sauvegarde du refresh token
    
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")



