

class NotFoundError(Exception):
    def __init__(self, ressource: list[str]):
        self.ressource = ressource


class DatabaseError(Exception):
    def __init__(self):
        pass

class ConflictError(Exception):
    def __init__(self, detail: str):
        self.detail = detail