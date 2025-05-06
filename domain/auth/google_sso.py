from datetime import timedelta
import os

from fastapi import APIRouter, HTTPException, Request
from fastapi_sso import GoogleSSO

from domain.auth.authentication_service import create_access_token, create_refresh_token
from domain.auth.refresh_token.refresh_token_model import RefreshToken
from domain.auth.refresh_token.refresh_token_repository import RefreshTokenRepository
from domain.user.user_services import UserServices
from domain.user.user_model import User
from domain.auth.token_schema import Token


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


# Utilisée pour désactiver l'exigence d'une connexion sécurisée (HTTPS) lors de l'utilisation de la bibliothèque oauthlib, qui est sous-jacente à fastapi_sso.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


google_sso = GoogleSSO(
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, f"{os.getenv('HOST')}/google/callback"
)


router = APIRouter(prefix="/google", tags=["auth"])


@router.get("/login")
async def google_login():
    async with google_sso:
        return await google_sso.get_login_redirect(
            params={"prompt": "consent", "access_type": "offline"}
        )


@router.get("/callback")
async def google_callback(request: Request):
    """Process login response from Google and return user info"""

    try:
        async with google_sso:
            user = await google_sso.verify_and_process(request)

        user_stored = await UserServices().get_by_email(user.email)
        if not user_stored:
            user_to_add = User(
                email=user.email,
            )
            user_stored = await UserServices().create_with_provider(user_to_add, provider=user.provider)

        access_token = create_access_token(
            data={"sub": user_stored.id},
            expires_delta=timedelta(
                minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
            ),
        )

        request_ip = request.client.host
        request_user_agent = request.headers.get("User-Agent")

        refresh_token = create_refresh_token(
            data={"sub": user_stored.id},
            expires_delta=timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))),
        )

        await RefreshTokenRepository().save(
            RefreshToken(
                user_id=user_stored.id,
                refresh_token=refresh_token,
                ip_address=request_ip,
                user_agent=request_user_agent,
            )
        )

        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
