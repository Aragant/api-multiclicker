from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Form, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from authentication import SESSION_COOKIE_NAME, authenticate_user, create_access_token
from schemas import User, UserSignUp
from infrastructure.database.database import get_db
import user_db_crud as db_crud


router = APIRouter(prefix="/auth")

@router.post("/sign_up", response_model=User, summary="Register a user", tags=["Auth"])
def create_user(user_signup: UserSignUp, db: Session = Depends(get_db)):
    """
    Registers a user.
    """
    try:
        user_created = db_crud.add_user(db, user_signup)
        return user_created
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")
        
        
@router.post("/login", summary="Login as a user", tags=["Auth"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Logs in a user.
    """
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password, provider='local')
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password.")
    try:
        access_token = create_access_token(username=user.username, provider='local')
        # response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response = JSONResponse(content={"message": "Login successful"})
        
        # Set the cookie
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=access_token,
            httponly=True,  # Prevent JavaScript access to the cookie
            max_age=3600,  # Cookie expiration time in seconds
            expires=3600,  # Same as max_age
            secure=True,   # Send cookie only over HTTPS
            samesite="Strict"  # Prevent CSRF in some cases
        )
        
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.post("/logout", summary="Logout a user", tags=["Auth"])
def logout():
    """
    Logout a user.
    """
    try:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.delete_cookie(SESSION_COOKIE_NAME)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")