from dotenv import load_dotenv
from fastapi import FastAPI  
import uvicorn


from infrastructure.fastapi.set_middleware import set_middleware
from infrastructure.logging.logging_config import logger
from infrastructure.fastapi.lifespan import lifespan
from conf.app_conf import AppConf


app = FastAPI(
title=AppConf.TITLE,
description=AppConf.DESCRIPTION,
version=AppConf.VERSION,
lifespan=lifespan
)


set_middleware(app)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)






@app.get("/")
async def root():
    logger.info("Requête reçue sur la route '/'")
    return {"message": "Hello World"}