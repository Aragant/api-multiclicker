from datetime import timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from domain.auth.authentication_service import authenticate_user, create_access_token, create_refresh_token
from domain.auth.refresh_token.refresh_token_model import RefreshToken
from domain.auth.refresh_token.refresh_token_repository import RefreshTokenRepository

from domain.auth.token_schema import Token


router = APIRouter(prefix="/auth", tags=["auth"])




@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    request_ip = request.client.host
    request_user_agent = request.headers.get("User-Agent")
    
    refresh_token = create_refresh_token(
        data={"sub": user.id}, expires_delta=timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
    )
    
    await RefreshTokenRepository().save(RefreshToken(user_id=user.id, refresh_token=refresh_token, ip_address=request_ip, user_agent=request_user_agent))
    
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, request: Request):
    token_entry = await RefreshTokenRepository().get_by_refresh_token(refresh_token)
    if not token_entry:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    request_ip = request.client.host
    request_user_agent = request.headers.get("User-Agent")
    
    if token_entry.ip_address != request_ip or token_entry.user_agent != request_user_agent:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Suspicious activity detected")

    # Générer un nouveau access token
    new_access_token = create_access_token(data={"sub": token_entry.user_id}, expires_delta=timedelta(minutes=10))

    return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.delete("/logout")
async def logout(refresh_token: str):
    await RefreshTokenRepository().delete_by_refresh_token(refresh_token)
    return {"message": "Refresh token revoked"}




