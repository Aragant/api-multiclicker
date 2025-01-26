

from fastapi import Request
from fastapi.responses import JSONResponse
from infrastructure.error.error import DatabaseError, NotFoundError


def setup_exepction_handlers(app):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(content={"NotFoundError: ": f"{exc.ressource} not found"}, status_code=404)
    
    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        return JSONResponse(content={"DatabaseError": "Database error"}, status_code=500)