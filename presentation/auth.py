from fastapi import APIRouter

from infrastructure.error import NotFoundError



router = APIRouter(prefix="/auth")


@router.get("/")
async def root():
    raise NotFoundError(ressource="root")