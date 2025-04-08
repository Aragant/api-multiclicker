from fastapi import Request
from fastapi.responses import JSONResponse
from infrastructure.error.error import DatabaseError, DuplicateEntryError, NotFoundError, ForbiddenError

def setup_exepction_handlers(app):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            content={"NotFoundError: ": f"{exc.ressource} not found"}, status_code=404
        )

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        return JSONResponse(
            content={"DatabaseError": "Database error", "details": f"{exc}"},
            status_code=500,
        )
    
    @app.exception_handler(DuplicateEntryError)
    async def duplicate_entry_handler(request: Request, exc: DuplicateEntryError):
        return JSONResponse(
            status_code=409,  # Code HTTP 409 pour conflit
            content={
                "error": "Duplicate entry",
                "details": str(exc) 
            }
        )
    @app.exception_handler(ForbiddenError)
    async def forbidden_error_handler(request: Request, exc: ForbiddenError):
        return JSONResponse(
            status_code=403,
            content={
                "error": "Forbidden",
                "message": str(exc) 
            }
        )
