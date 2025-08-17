from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio

from infrastructure.error.exeption_handler import setup_exepction_handlers
from infrastructure.fastapi.set_middleware import set_middleware
from infrastructure.fastapi.lifespan import lifespan
from conf.app_conf import AppConf

from domain.auth.auth_presentation import router as auth_router
from domain.user.user_presentation import router as user_router
from domain.guild.guild_presentation import router as guild_router
from domain.auth.google_sso import router as google_router
from domain.websocket.ws_presentation import router as websocket_router

rest_router = [auth_router, google_router, user_router, guild_router, websocket_router]

load_dotenv()

app = FastAPI(
    title=AppConf.TITLE,
    description=AppConf.DESCRIPTION,
    version=AppConf.VERSION,
    lifespan=lifespan,
)


set_middleware(app)

setup_exepction_handlers(app)


for router in rest_router:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9999,
        reload=True,
        ssl_certfile="/home/ccddr/localhost+2.pem",
        ssl_keyfile="/home/ccddr/localhost+2-key.pem",
    )
