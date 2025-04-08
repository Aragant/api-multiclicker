

class NotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DatabaseError(Exception):
    def __init__(self):
        pass
      
class ConflictError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        
class DuplicateEntryError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class ForbiddenError(Exception):
    def __init__(self, message: str):
        super().__init__(message)