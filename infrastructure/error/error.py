from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    def __init__(self, ressource: list[str]):
        self.ressource = ressource

class DatabaseError(Exception):
    def __init__(self):
        pass


