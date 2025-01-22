import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request  
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy.orm import Session
from importlib.metadata import version
from fastapi.staticfiles import StaticFiles

from authentication import get_current_user
from infrastructure.fastapi.set_middleware import set_middleware
from infrastructure.logging.logging_config import logger
from infrastructure.fastapi.lifespan import lifespan
from conf.app_conf import AppConf
from infrastructure.database.database import get_db
from schemas import User
import user_db_crud as db_crud
from presentation import auth


load_dotenv()
parent_directory = Path(__file__).parent
templates_path = parent_directory / "templates"
templates = Jinja2Templates(directory=templates_path)


app = FastAPI(
title=AppConf.TITLE,
description=AppConf.DESCRIPTION,
version=AppConf.VERSION,
lifespan=lifespan
)


set_middleware(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)




@app.get("/", response_class=HTMLResponse, summary="Home page")
def home_page(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Returns all users.
    """
    versions = {
        "fastapi_version": version('fastapi'),
        "fastapi_sso_version": version('fastapi_sso')
    }
    try:
        if user is not None:
            users_stats = db_crud.get_users_stats(db)
            response = templates.TemplateResponse("index.html", {"request": request, "user": user, "users_stats": users_stats, **versions})
        else:
            response = templates.TemplateResponse("login.html", {"request": request, **versions})
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@app.get("/privacy_policy", response_class=HTMLResponse, summary="Privacy Policy")
def privacy_policy(request: Request):
    """
    Returns privacy policy page.
    """
    try:
        response = templates.TemplateResponse(
            "privacy_policy.html",
            {
                "request": request,
                "host": os.getenv('HOST'),
                "contact_email": os.getenv('CONTACT_EMAIL')
            }
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)


