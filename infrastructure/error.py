from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    def __init__(self, ressource: str):
        self.ressource = ressource



