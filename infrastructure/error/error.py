class NotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

class DatabaseError(Exception):
    def __init__(self):
        pass
      
class ConflictError(Exception):
    def __init__(self, message: str):
        self.message = message
        
class DuplicateEntryError(Exception):
    def __init__(self, type: str, message: str):
        self.message = message
        self.type = type

class ForbiddenError(Exception):
    def __init__(self, message: str):
        self.message = message
        
class UnprocessableEntityError(Exception):
    def __init__(self, type: str, message: str):
        self.message = message
        self.type = type