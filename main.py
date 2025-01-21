from dotenv import load_dotenv
from fastapi import FastAPI  
import uvicorn


from infrastructure.fastapi.set_middleware import set_middleware
from infrastructure.logging.logging_config import logger
from infrastructure.fastapi.lifespan import lifespan




    
    
description = """
Example API to demonstrate SSO login in fastAPI
"""
    
app = FastAPI(
title='SSO login example API',
description=description,
version="1.0.0",
docs_url="/v1/documentation",
redoc_url="/v1/redocs",
lifespan=lifespan
)


set_middleware(app)

@app.get("/")
async def root():
    logger.info("Requête reçue sur la route '/'")
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9999)