

from fastapi import Request
from fastapi.responses import JSONResponse
from infrastructure.error.error import NotFoundError


def setup_exepction_handlers(app):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(content={"NotFoundError: ": f"{exc.ressource} not found"}, status_code=404)