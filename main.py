from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn



from infrastructure.error.exeption_handler import setup_exepction_handlers
from infrastructure.fastapi.set_middleware import set_middleware
from infrastructure.logging.logging_config import logger
from infrastructure.fastapi.lifespan import lifespan
from conf.app_conf import AppConf
from presentation import auth


load_dotenv()

app = FastAPI(
title=AppConf.TITLE,
description=AppConf.DESCRIPTION,
version=AppConf.VERSION,
lifespan=lifespan
)


set_middleware(app)

setup_exepction_handlers(app)
app.include_router(auth.router)



if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)


