

class NotFoundError(Exception):
    def __init__(self, ressource: list[str]):
        self.ressource = ressource


class DatabaseError(Exception):
    def __init__(self):
        pass

class DuplicateEntryError(Exception):
    def __init__(self, message: str):
        super().__init__(message)